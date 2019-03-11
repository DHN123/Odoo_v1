odoo.define('tree_menu.tree_view_button', function(require){
"use strict";


var core = require('web.core');
var ListView = require('web.ListView');
var QWeb = core.qweb;


ListView.include({
        render_button: function($node){
        var self = this;
        this._super($node).find('o_list_send_data').click(this.proxy('concrete_pump_category_action'));
        },
        concrete_pump_category_action: function(){

        this.do_action({
            type: "ir.action.act_window",
            name: "Concrete Pump Attributes Categories",
            res_model: "concrete.pump.category",
            views:[[false,'form']],
            target: 'current',
            view_type: 'form',
            view_mode: 'form',
            flags: {'form': {'action_buttons': true, 'option': {'mode': 'edit'}}}
        });
        return {'type': 'ir.action.client','tag': 'reload',}}
});
});