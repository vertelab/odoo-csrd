/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";
import { formView } from "@web/views/form/form_view";
import { FormController } from "@web/views/form/form_controller";
import { FormViewDialog } from '@web/views/view_dialogs/form_view_dialog';
import { useService } from "@web/core/utils/hooks";
import Wysiwyg from 'web_editor.wysiwyg';
import { parseHTML, preserveCursor } from '@web_editor/js/editor/odoo-editor/src/OdooEditor';

const { Component } = owl;


Wysiwyg.include({

    async createPolicy() {
        const self = this;

        self._rpc({
            model: 'ir.model.data',
            method: 'check_object_reference',
            args: ['csrd_policy_support', 'view_csrd_esrs_policy_form']
        }).then(function (res_id) {
            if (res_id) {
                self.do_action({
                    type: "ir.actions.act_window",
                    target: "new",
                    name: "Create AI Policy",
                    res_model: "csrd.esrs",
                    res_id: self.options.recordInfo.res_id,
                    views: [[res_id[1], "form"]],
                })
            }
        })
    },

    _getPowerboxOptions: function () {
        const options = this._super.apply(this, arguments);
        const {commands, categories} = options;
        categories.push({ name: 'AI', priority: 50 });
        commands.push({
            category: 'AI',
            name: _t('Create Policy'),
            priority: 10,
            description: _t('Prompt AI for CSRD Policy'),
            fontawesome: 'fa-bot',
            callback: async() => {
                await this.createPolicy()
            },
        });

        return {...options, commands, categories};
    },

});