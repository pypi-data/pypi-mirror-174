import json
import logging
from daggerml.__about__ import __version__  # noqa: F401
from daggerml._config import DML_API_ENDPOINT
from http.client import HTTPConnection, HTTPSConnection
from urllib.parse import urlparse


logger = logging.getLogger(__name__)


class DmlError(Exception):
    def __init__(self, msg):
        super().__init__(msg)
        self.msg = msg


class ApiError(DmlError):
    pass


class DagError(DmlError):
    pass


class NodeError(DmlError):
    def __init__(self, node_id, msg):
        super().__init__(msg)
        self.node_id = node_id

    def __repr__(self):
        return f'NodeError({self.node_id}, {self.msg})'


def _api(api_, op, group=None, **kwargs):
    try:
        url = urlparse(DML_API_ENDPOINT)
        scheme = url.scheme or 'http'
        host = url.hostname or 'localhost'
        port = url.port or 80
        path = url.path or '/'
        conn = (HTTPConnection if scheme == 'http' else HTTPSConnection)(host, port)
        headers = {'content-type': 'application/json', 'accept': 'application/json'}
        if isinstance(group, str):
            headers['X-DaggerML-Group'] = group
        conn.request('POST', path, json.dumps(dict(api=api_, op=op, **kwargs)), headers)
        resp = conn.getresponse()
        if resp.status != 200:
            raise ApiError(f'{resp.status} {resp.reason}')
        resp = json.loads(resp.read())
        if resp['status'] != 'ok':
            err = resp['error']
            if err['context']:
                logger.error('api error: %s', '\n'.join(err['context']))
            raise ApiError(f'{err["code"]}: {err["message"]}')
        return resp['result']
    except KeyboardInterrupt:
        raise
    except ApiError:
        raise
    except Exception as e:
        raise ApiError(f'{e.__class__.__name__}: {str(e)}')


def list_dags(name=None):
    return _api('dag', 'list', name=name)


def describe_dag(dag_id):
    return _api('dag', 'describe', dag_id=dag_id)


def daggerml():
    from time import sleep
    from collections.abc import Mapping
    from weakref import WeakKeyDictionary
    from dataclasses import dataclass
    from typing import NewType, Optional
    from uuid import uuid4

    @dataclass(frozen=True)
    class Resource:
        id: str
        parent: Optional[NewType('Resource', None)]

    def data_to_resource(data):
        if data is None:
            return None
        return Resource(data['id'], data_to_resource(data['parent']))

    def resource_to_data(rsrc):
        if rsrc is None:
            return None
        return {'id': rsrc.id, 'parent': resource_to_data(rsrc.parent)}

    def to_data(py, dag=None):
        if isinstance(py, Node):
            return {'type': 'ref', 'value': {'node_id': py.id}}
        if callable(py):
            if dag is None:
                raise RuntimeError(
                    'cannot call `to_data` on a local function without a dag argument'
                )
            fn_id = py.__qualname__
            if fn_id == '<lambda>':
                fn_id += uuid4().hex
            fn_id = py.__module__ + ':' + fn_id
            py = [Node(dag, dag.executor_id), fn_id]
        if isinstance(py, list) or isinstance(py, tuple):
            return {'type': 'list', 'value': [to_data(x, dag) for x in py]}
        elif isinstance(py, dict) or isinstance(py, Mapping):
            if not all([isinstance(x, str) for x in py]):
                raise TypeError('map datum keys must be strings')
            return {'type': 'map', 'value': {k: to_data(v, dag) for (k, v) in py.items()}}
        elif isinstance(py, type(None)):
            return {'type': 'scalar', 'value': {'type': 'null'}}
        elif isinstance(py, str):
            return {'type': 'scalar', 'value': {'type': 'string', 'value': str(py)}}
        elif isinstance(py, int):
            return {'type': 'scalar', 'value': {'type': 'int', 'value': str(py)}}
        elif isinstance(py, float):
            return {'type': 'scalar', 'value': {'type': 'float', 'value': str(py)}}
        elif isinstance(py, Resource):
            return {'type': 'resource', 'value': resource_to_data(py)}
        else:
            raise ValueError('unknown type: ' + type(py))

    def from_data(res):
        t = res['type']
        v = res['value']
        if t == 'list':
            return tuple([from_data(x) for x in v])
        elif t == 'map':
            return {k: from_data(x) for (k, x) in v.items()}
        elif t == 'scalar':
            t = v['type']
            v = v.get('value')
            if t == 'int':
                return int(v)
            elif t == 'float':
                return float(v)
            elif t == 'string':
                return str(v)
            elif t == 'null':
                return None
            else:
                raise ValueError('unknown scalar type: ' + t)
        elif t == 'resource':
            return data_to_resource(v)
        else:
            raise ValueError('unknown type: ' + t)

    CACHE = WeakKeyDictionary()

    @dataclass(frozen=True)
    class Node:
        dag: NewType("Dag", None)
        id: str

        def __len__(self):
            return len(self.dag.to_py(self))

        def __getitem__(self, key):
            f = Node(self.dag, self.dag.get_fn)
            resp = f(self, key)
            cached = CACHE.get(self)
            if cached is not None:
                if isinstance(key, Node):
                    key = key.to_py()
                CACHE[resp] = cached[key]
            return resp

        def __call__(self, *args, block=True):
            args = [self.dag.from_py(x) for x in args]
            if callable(CACHE.get(self)):
                resp = _api('dag', 'put_fnapp_and_claim', dag_id=self.dag.id,
                            ttl=0, secret=self.dag.secret,
                            expr=[self.id] + [x.id for x in args])
                if resp['success']:
                    return Node(self.dag, resp['node_id'])
                if resp['error'] is not None:
                    logger.debug('ignoring error: %s', json.dumps(resp['error']))
                try:
                    result = CACHE[self](*args)
                    resp2 = _api('node', 'commit_node',
                                 node_id=resp['node_id'],
                                 secret=self.dag.secret,
                                 token=resp['refresh_token'],
                                 data=to_data(result, dag=self.dag))
                    assert resp2['finalized'], 'failed to finalize node'
                except Exception as e:
                    err = {'message': str(e)}
                    _api('node', 'fail_node', secret=self.dag.secret,
                         node_id=resp['node_id'], token=resp['refresh_token'],
                         error=err)
                    raise NodeError(resp['node_id'], err)
                n = Node(self.dag, resp['node_id'])
                CACHE[n] = result
                return n
            expr = [self.id] + [x.id for x in args]
            waiter = NodeWaiter(self.dag, expr)
            if not block:
                return waiter
            waiter.wait(2)
            return waiter.result

        def to_py(self):
            return self.dag.to_py(self)

        def __repr__(self):
            return f'Node({self.dag.name},{self.dag.version},{self.id})'

    @dataclass
    class NodeWaiter:
        def __init__(self, dag, expr):
            self.dag = dag
            self.expr = expr
            self._result = None
            self.check()

        def check(self):
            self._resp = _api('dag', 'put_fnapp', dag_id=self.dag.id,
                              expr=self.expr, secret=self.dag.secret)
            return self.result

        @property
        def node_id(self):
            return self._resp['node_id']

        @property
        def result(self):
            if self._resp['success']:
                return Node(self.dag, self.node_id)
            if self._resp['error'] is not None:
                logger.debug('ignoring error: %s', json.dumps(self._resp['error']))
                raise NodeError(self.node_id, self._resp['error'])
            return

        def wait(self, dt=5):
            while self.result is None:
                sleep(dt)
                self.check()
            return self.result

    def get_dag_by_name_version(dag_name, version='latest'):
        tmp = _api('dag', 'get_dag_by_name_version', name=dag_name, version=version)
        if tmp is not None:
            tmp = tmp['result']
        return tmp

    @dataclass(frozen=True)
    class Dag:
        id: str
        name: str = None
        version: int = None
        group: str = None
        expr_id: str = None
        get_fn: str = None
        executor_id: str = None
        secret: str = None

        def __post_init__(self):
            if self.executor_id is not None:
                object.__setattr__(self, 'executor', Node(self, self.executor_id).to_py())
            pass

        @classmethod
        def new(cls, name, group='test0'):
            resp = _api('dag', 'create_dag', name=name, group=group)
            return cls(**resp, group=group)

        def from_py(self, py):
            if isinstance(py, Node):
                return py
            res = _api('dag', 'put_literal', dag_id=self.id, data=to_data(py, self),
                       group=self.group, secret=self.secret)
            node = Node(self, res['node_id'])
            if node not in CACHE:
                CACHE[node] = py
            return node

        def to_py(self, node):
            if node.dag != self:
                raise ValueError('node does not belong to dag')
            if node in CACHE:
                return CACHE[node]
            py = from_data(_api('node', 'get_node', node_id=node.id,
                                group=self.group, secret=self.secret))
            CACHE[node] = py
            return py

        def fail(self, result=None):
            kwargs = {}
            if result is not None:
                kwargs['result'] = self.from_py(result).id
            if not _api('dag', 'fail_dag', dag_id=self.id, group=self.group,
                        secret=self.secret, **kwargs)['success']:
                raise DagError('Failed to fail dag')
            return

        def commit(self, result):
            result = self.from_py(result)
            if not _api('dag', 'commit_dag', dag_id=self.id, result=result.id,
                        group=self.group, secret=self.secret)['success']:
                raise DagError('Failed to commit dag')
            return

        def load(self, dag_name, version='latest'):
            node_id = get_dag_by_name_version(dag_name, version)
            if node_id is None:
                raise DagError('No such dag/version: %s / %r' % (dag_name, version))
            res = _api('dag', 'put_load', dag_id=self.id,
                       node_id=node_id, secret=self.secret)
            return Node(self, res['node_id'])

        def create_resource(self):
            res = _api('dag', 'create_resource', dag_id=self.id,
                       group=self.group, secret=self.secret)
            return Node(self, res['node_id']), res['secret']

        def __repr__(self):
            return f'Dag({self.name},{self.version})'

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, exc_traceback):
            if exc_type is not None:
                err = None
                if exc_type == NodeError:
                    err = Node(self, exc_value.node_id)
                self.fail(err)
                return True  # FIXME remove this to not catch these errors

    def claim_execution(executor, secret, ttl, node_id=None, group='test0'):
        resp = _api('node', 'claim_node', executor=resource_to_data(executor),
                    ttl=ttl, node_id=node_id, group=group, secret=secret)
        resp['group'] = group
        return resp

    return Resource, Dag, Node, claim_execution


Resource, Dag, Node, claim_execution = daggerml()
del daggerml
