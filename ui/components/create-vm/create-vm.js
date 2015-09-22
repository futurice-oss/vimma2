Polymer({
  is: 'create-vm',

  behaviors: [VimmaBehaviors.Equal],

  observers: [
  ],

  properties: {
    _expanded: {
      type: Boolean,
      notify: true,
      value: false
    },

    _toggleClass: {
      type: String,
      computed: 'toggleClass(_expanded)'
    },

    createUrl: {
      type: String,
      value: '#'
    },

    projectsUrl: {
      type: String,
      value: vimmaApiProjectList
    },

    providersDummyUrl: {
      type: String,
      value: vimmaApiDummyProviderList
    },

    providersAwsUrl: {
      type: String,
      value: vimmaApiAwsProviderList
    },

    providers: {
      type: Array,
      computed: 'computeProviders(providersDummy, providersAws)'
    },

    schedulesUrl: {
      type: String,
      value: vimmaApiScheduleList
    },
    schedules: Array
  },

  computeProviders: function(dummy, aws) {
    return [].concat(dummy.results).concat(aws.results);
  },

  ready: function() {
  },

  scheduleSelected: function(k, detail) {
    this.$$('#schedule').value = k.currentTarget.dataItem.id;
    this.chosen(k.currentTarget, '.schedule-container div.box')
  },

  providerSelected: function(k, detail) {
    this.$$('#provider').value = k.currentTarget.dataItem.id;
    this.$$('#config').value = k.currentTarget.dataConfig.id;
    this.chosen(k.currentTarget, '.provider-container div.box')
    this.createUrl = url(k.currentTarget.dataConfig.content_type.app_label+'vm-create');
  },

  chosen: function(el, container) {
    $(container).removeClass('chosen');
    $(el).toggleClass('chosen');
  },

  _toggle: function() {
    this._expanded = !this._expanded;
  },

  toggleClass: function(expanded) {
    return (expanded) ? 'visible' : 'hidden';
  },

  submitForm: function() {
    f = this.$$('#create-vm-form');
    f._requestBot.headers = {'X-CSRFToken': $.cookie('csrftoken')};
    f.submit();
    // TODO: listen to iron-form-response to fire vm-created
    this.fire('vm-created');
  }
});
