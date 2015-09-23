Polymer({
  is: 'vm-schedule',

  behaviors: [VimmaBehaviors.Equal],

  properties: {
    vm: {
      type: Object,
      observer: '_vmidChanged'
    },

    _schedules: Array,

    _newSchedId: Number,

    _unsavedChanges: {
      type: Boolean,
      computed: '_computeUnsavedChanges(_vm, _newSchedId)'
    }
  },

  scheduleUrl: function() {
    return vimmaApiScheduleList;
  },

  _vmidChanged: function(newV, oldV) {
  },

  _reload: function() {
  },

  _scheduleChanged: function(ev) {
    this._newSchedId = this._schedules[ev.target.selectedIndex].id;
  },

  _vmChanged: function(newV, oldV) {
    this._newSchedId = newV.schedule;
  },

  _computeUnsavedChanges: function(vm, newSchedId) {
    return vm.schedule !== newSchedId;
  },
  _getButtonClass: function(unsavedChanges) {
    if (unsavedChanges) {
      return 'unsaved';
    }
    return '';
  },

  _save: function() {
    // TODO: save schedule
    // - reload on complete
  }
});
