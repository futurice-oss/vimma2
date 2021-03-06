Polymer({
    is: 'create-aws-firewall-rule',

    behaviors: [VimmaBehaviors.Equal],

    properties: {
        vmid: Number,
        _expanded: {
            type: Boolean,
            value: false
        },

        _protocol: {
            type: Object,
            value: awsFirewallRuleProtocolChoices[0]
        },
        _ports: {
            type: String,
            value: ''
        },
        _cidr_ip: {
            type: String,
            value: '0.0.0.0/0'
        },
        _protocolChoices: {
            type: Array,
            value: awsFirewallRuleProtocolChoices,
            readOnly: true
        },

        _createInFlight: Boolean,
        _createErr: String
    },

    _toggle: function() {
        this._expanded = !this._expanded;

        this._protocol = this.properties._protocol.value;
        this._ports = this.properties._ports.value;
        this._cidr_ip = this.properties._cidr_ip.value;
        this._createErr = '';
    },

    _protocolSelected: function(ev) {
        this._protocol = this._protocolChoices[ev.target.selectedIndex];
    },

    _create: function() {
        var ports = this._ports.split('-').map(function(s) {
            return parseInt(s, 10);
        });
        var data = {
            ip_protocol: this._protocol.value,
            from_port: ports[0],
            to_port: ports[ports.length - 1],
            cidr_ip: this._cidr_ip
        };

        this._createInFlight = true;

        $.ajax({
            url: vimmaEndpointCreateFirewallRule,
            type: 'POST',
            contentType: 'application/json; charset=UTF-8',
            headers: {
                'X-CSRFToken': $.cookie('csrftoken')
            },
            data: JSON.stringify({
                vmid: this.vmid,
                data: data
            }),
            complete: (function(data) {
                this._createInFlight = false;
            }).bind(this),
            success: (function(data) {
                this._createErr = '';
                this._toggle();
                this.fire('aws-firewall-rule-created');
            }).bind(this),
            error: (function() {
                var errorText = getAjaxErr.apply(this, arguments);
                this._createErr = errorText;
            }).bind(this)
        });
    }
});
