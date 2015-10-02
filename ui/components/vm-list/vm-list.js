(function() {
  var orderNameAsc = '+name',
    orderNameDesc = '-name',
    orderStateAsc = '+state',
    orderStateDesc = '-state',
    orderProjectAsc = '+project',
    orderProjectDesc = '-project',
    orderExpiryAsc = '+expiry',
    orderExpiryDesc = '-expiry';

  var compareFuncs = {};
  compareFuncs[orderNameAsc] = compareNameAsc;
  compareFuncs[orderNameDesc] = compareNameDesc;

  compareFuncs[orderStateAsc] = compareStateAsc;
  compareFuncs[orderStateDesc] = compareStateDesc;

  compareFuncs[orderProjectAsc] = compareProjectAsc;
  compareFuncs[orderProjectDesc] = compareProjectDesc;

  compareFuncs[orderExpiryAsc] = compareExpiryAsc;
  compareFuncs[orderExpiryDesc] = compareExpiryDesc;

  function compare(a, b) {
    if (a < b) {
      return -1;
    }
    if (a > b) {
      return 1;
    }
    return 0;
  }

  function compareNameAsc(a, b) {
    a = a.name.toLowerCase();
    b = b.name.toLowerCase();
    return compare(a, b);
  }

  function compareNameDesc(a, b) {
    return compareNameAsc(b, a);
  }

  function compareStateAsc(a, b) {
    // destroyed, off, on
    if (a.isDestroyed() != b.isDestroyed()) {
      return compare(b.isDestroyed(), a.isDestroyed());
    }
    if (a.isDestroyed()) {
      return 0;
    }
    return compare(a.isOn(), b.isOn());
  }

  function compareStateDesc(a, b) {
    return compareStateAsc(b, a);
  }

  function compareProjectAsc(a, b) {
    a = a.getProjectName().toLowerCase();
    b = b.getProjectName().toLowerCase();
    return compare(a, b);
  }

  function compareProjectDesc(a, b) {
    return compareProjectAsc(b, a);
  }

  function compareExpiryAsc(a, b) {
    a = new Date(a.getExpiryDate()).valueOf();
    b = new Date(b.getExpiryDate()).valueOf();
    return compare(a, b);
  }

  function compareExpiryDesc(a, b) {
    return compareExpiryAsc(b, a);
  }

  Polymer({
    is: 'vm-list',

    behaviors: [VimmaBehaviors.Equal],

    properties: {
      vmUrl: {
        type: String,
        computed: 'computeVmUrl(name)'
      },

      // load destroyed or non-destroyed VMs
      destroyed: {
        type: Boolean,
        value: false,
        observer: '_destroyedChanged'
      },

      vmData: {
        type: Object,
        notify: true,
        observer: 'vmDataChanged'
      },

      expanded: {
        type: Boolean,
        value: false
      },

      // avoid 3 nested ‘dom-if’s
      _showList: {
        type: Boolean,
        computed: '_computeShowList(_loading, _error, expanded)'
      },

      _headingIcon: {
        type: String,
        computed: '_computeHeadingIcon(expanded)'
      },
      _order: {
        type: String,
        value: orderNameAsc
      },
      _nameSortIcon: {
        type: String,
        computed: '_computeNameSortIcon(_order)'
      },
      _stateSortIcon: {
        type: String,
        computed: '_computeStateSortIcon(_order)'
      },
      _projectSortIcon: {
        type: String,
        computed: '_computeProjectSortIcon(_order)'
      },
      _expirySortIcon: {
        type: String,
        computed: '_computeExpirySortIcon(_order)'
      },
      _nameClass: {
        type: String,
        computed: '_computeNameClass(_order)'
      },
      _stateClass: {
        type: String,
        computed: '_computeStateClass(_order)'
      },
      _projectClass: {
        type: String,
        computed: '_computeProjectClass(_order)'
      },
      _expiryClass: {
        type: String,
        computed: '_computeExpiryClass(_order)'
      },
      sortedVms: {
        type: Array,
        computed: '_sort(vms, _order)'
      },
      newVm: {
        type: Object,
        computed: '_created(vmCreated, name)'
      }
    },

    computeVmUrl: function(name) {
      return url(name+'vm-list');
    },

    vmDataChanged: function(newV, oldV) {
      this.$.projectAjax.url = '/api/projects/' + newV.project;
      this.$.projectAjax.generateRequest();
    },

    ready: function() {
    },

    _created: function(ev, name) {
      if(ev.detail.provider==name) {
        this.reload();
        // TODO: could highlight the newly created VM
      }
    },

    reload: function() {
      this.$.vmAjax.generateRequest();
    },

    _destroyedChanged: function(newV, oldV) {
      //this.reload();
    },

    _toggle: function() {
      this.expanded = !this.expanded;
    },

    _computeShowList: function(loading, error, expanded) {
      return !loading && !error && expanded;
    },

    _computeHeadingIcon: function(expanded) {
      if (expanded) {
        return 'expand-less';
      }
      return 'expand-more';
    },
    /* Call VMModel methods (we can't do it in the template directly). */
    _getExpiryDate: function(vm) {
      return vm.getExpiryDate();
    },
    _getProjectName: function(vm) {
      return vm.getProjectName();
    },
    _isDestroyed: function(vm) {
      return vm.isDestroyed();
    },

    _sort: function(vms, order) {
      return vms.results.slice().sort(compareFuncs[order]);
    },
    _toggleOrder: function(default_, alternate) {
      if (this._order == default_) {
        this._order = alternate;
      } else {
        this._order = default_;
      }
    },
    _sortByName: function() {
      this._toggleOrder(orderNameAsc, orderNameDesc);
    },
    _sortByState: function() {
      this._toggleOrder(orderStateDesc, orderStateAsc);
    },
    _sortByProject: function() {
      this._toggleOrder(orderProjectAsc, orderProjectDesc);
    },
    _sortByExpiry: function() {
      this._toggleOrder(orderExpiryAsc, orderExpiryDesc);
    },
    // arrow-drop-up if order if ascOrder, -down if descOrder, else ''.
    _computeSortIcon: function(order, ascOrder, descOrder) {
      if (order == ascOrder) {
        return 'arrow-drop-up';
      }
      if (order == descOrder) {
        return 'arrow-drop-down';
      }
      return '';
    },
    _computeNameSortIcon: function(order) {
      return this._computeSortIcon(order, orderNameAsc, orderNameDesc);
    },
    _computeStateSortIcon: function(order) {
      return this._computeSortIcon(order, orderStateAsc, orderStateDesc);
    },
    _computeProjectSortIcon: function(order) {
      return this._computeSortIcon(order,
        orderProjectAsc, orderProjectDesc);
    },
    _computeExpirySortIcon: function(order) {
      return this._computeSortIcon(order,
        orderExpiryAsc, orderExpiryDesc);
    },
    _computeClass: function(order, selectedOrders) {
      var i, n = selectedOrders.length;
      for (i = 0; i < n; i++) {
        if (order == selectedOrders[i]) {
          return 'ordering-selected';
        }
      }
      return '';
    },
    _computeNameClass: function(order) {
      return this._computeClass(order, [orderNameAsc, orderNameDesc]);
    },
    _computeStateClass: function(order) {
      return this._computeClass(order, [orderStateAsc, orderStateDesc]);
    },
    _computeProjectClass: function(order) {
      return this._computeClass(order, [orderProjectAsc, orderProjectDesc]);
    },
    _computeExpiryClass: function(order) {
      return this._computeClass(order, [orderExpiryAsc, orderExpiryDesc]);
    },

    _vmExpanded: function(ev) {},
    _vmCollapsed: function(ev) {},

    _sayTopBarOne: function(destroyed) {
      if (destroyed) {
        return 'destroyed';
      }
      return 'active';
    }
  });
})();
