'use strict';

/** load client folder*/

exports.get = {
  handler: {
    directory: {
      path: '../client/',
      index: true
    }
  }
};
