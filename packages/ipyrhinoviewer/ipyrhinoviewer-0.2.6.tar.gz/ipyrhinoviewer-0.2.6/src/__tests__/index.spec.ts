// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

// Add any needed widget imports here (or from controls)
// import {} from '@jupyter-widgets/base';

import { createTestModel } from './utils';

import { resolveUrl, RhinoModel } from '..';

describe('test resolve url', () => {
  it('correct absolute path in jupyterlab', () => {
    const path = '/test/test.3dm';
    window = Object.create(window);
    const url =
      'http://localhost:8080/user/j106930/lab/tree/test/Introduction%20to%20Python.ipynb';
    Object.defineProperty(window, 'location', {
      value: {
        href: url,
      },
    });

    expect(resolveUrl(path)).toEqual(
      'http://localhost:8080/user/j106930/tree/test/test.3dm'
    );
  });
  it('correct absolute path in nbclassic', () => {
    const path = '/test/test.3dm';
    window = Object.create(window);
    const url =
      'http://localhost:8080/notebooks/test/Introduction%20to%20Python.ipynb';
    Object.defineProperty(window, 'location', {
      value: {
        href: url,
      },
    });
    expect(resolveUrl(path)).toEqual(
      'http://localhost:8080/tree/test/test.3dm'
    );
  });
  it('correct relative path in jupyterlab', () => {
    const path = 'test.3dm';
    window = Object.create(window);
    const url =
      'http://localhost:8080/user/j106930/lab/tree/test/Introduction%20to%20Python.ipynb';
    Object.defineProperty(window, 'location', {
      value: {
        href: url,
      },
    });

    expect(resolveUrl(path)).toEqual(
      'http://localhost:8080/user/j106930/tree/test/test.3dm'
    );
  });
  it('correct relative path in nbclassic', () => {
    const path = 'test.3dm';
    window = Object.create(window);
    const url =
      'http://localhost:8080/notebooks/test/Introduction%20to%20Python.ipynb';
    Object.defineProperty(window, 'location', {
      value: {
        href: url,
      },
    });
    expect(resolveUrl(path)).toEqual(
      'http://localhost:8080/tree/test/test.3dm'
    );
  });
});

describe('Rhino', () => {
  describe('ExampleModel', () => {
    it('should be creatable', () => {
      const model = createTestModel(RhinoModel);
      expect(model).toBeInstanceOf(RhinoModel);
      expect(model.get('path')).toEqual('');
    });

    it('should be creatable with a value', () => {
      const state = { path: '/test.3dm' };
      const model = createTestModel(RhinoModel, state);
      expect(model).toBeInstanceOf(RhinoModel);
      expect(model.get('path')).toEqual('/test.3dm');
    });
  });
});
