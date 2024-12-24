// Copyright (c) 2024, Aerele and contributors
// For license information, please see license.txt

frappe.ui.form.on("Chatbot Message Template", {
	refresh(frm) {
        frm.set_query("print_format", function (doc) {
			return {
				filters: {
					"doc_type": frm.doc.default_doctype
				},
			};
		});
	},
});
