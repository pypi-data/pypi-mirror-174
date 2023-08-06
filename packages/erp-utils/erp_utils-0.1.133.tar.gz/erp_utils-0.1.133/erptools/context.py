import copy
import sys
from datetime import datetime

from .storage import ResourcesStorage


class TemplateContext:
    def __init__(self):
        self._order_api = None

        self.values_map = {
            'order_product_total': self._get_order_product_total,
            'order_product_installed': self._get_order_product_installed,
            'cutlist_quotes': self._get_cutlist_quotes,
            'cutlist_orders': self._get_cutlist_orders,
            'cutlist_deficiencies': self._get_cutlist_deficiencies,
            'account': self._get_account,
            'account_group': self._get_account_group,
            'account_group_type': self._get_account_group_type,
            'blank_checkbox': self._get_blank_checkbox,
            'business_legal_name': self._get_business_legal_name,
            'business_trade_name': self._get_business_trade_name,
            'checkbox': self._get_checkbox,
            'client': self._get_client,
            'client_cognito': self._get_client_cognito,
            'client_email': self._get_client_email,
            'client_name': self._get_client_name,
            'client_first_name': self._get_client_first_name,
            'client_last_name': self._get_client_last_name,
            'cnc_items': self._get_cnc_items,
            'cnc_data': self._get_cnc_data,
            'deficiency_item': self._get_deficiency_item,
            'company_address': self._get_company_address,
            'company_city': self._get_company_city,
            'company_email': self._get_company_email,
            'company_name': self._get_company_name,
            'company_postal_code': self._get_company_postal_code,
            'company_province': self._get_company_province,
            'date': self._get_date,
            'deficiency_items': self._get_deficiency_items,
            'delivery_questionnaire_hash': self._get_delivery_questionnaire_hash,
            'delivery_questionnaire_link': self._get_delivery_questionnaire_link,
            'delivery_questionnaire_pdf_filename': self._get_delivery_questionnaire_pdf_filename,
            'delivery_questionnaire_pdf_path': self._get_delivery_questionnaire_pdf_path,
            'extra_charges': self._get_extra_charges,
            "fabric_calc": self._get_fabric_calc,
            "fabric_coverage": self._get_fabric_coverage,
            'generated_files_folder': self._get_generated_path_files_folder,
            'generated_installer_folder': self._get_generated_path_installer_folder,
            'generated_installer_json': self._get_generated_path_installer_json,
            'generated_installer_pdf': self._get_generated_path_installer_pdf,
            'generated_shop_folder': self._get_generated_path_shop_folder,
            'generated_shop_json': self._get_generated_path_shop_json,
            'generated_shop_pdf': self._get_generated_path_shop_pdf,
            'group': self._get_group,
            'groups': self._get_group,
            'quote_groups': self._get_quote_groups,
            'installer_payment_pickup': self._get_installer_payment_pickup,
            'invoice': self._get_invoice,
            'invoice_total': self._get_invoice_total,
            'job_name': self._get_job_title,
            'job_title': self._get_job_title,
            'lead_days': self._get_lead_days,
            'order': self._get_order,
            'order_id': self._get_order_id,
            'order_number': self._get_order_number,
            'order_products': self._get_order_products,
            'order_products_with_options': self._get_order_products_with_options,
            'order_product': self._get_order_product,
            'outside_paint_products': self._get_outside_paint_products,
            'packing_slip_pdf_filename': self._get_packing_slip_pdf_filename,
            'packing_slip_pdf_path': self._get_packing_slip_pdf_path,
            'payments': self._get_payments,
            'payments_outstanding': self._get_payments_outstanding,
            'payments_total': self._get_payments_total,
            'pretax': self._get_pretax,
            'product_total': self._get_product_total,
            'products': self._get_products,
            'project': self._get_project,
            'project_directory': self._get_project_directory,
            'project_id': self._get_project_id,
            'customer_po': self._get_customer_po,
            'proforma': self._get_proforma,
            'proforma_id': self._get_proforma_id,
            'purchase_order': self._get_purchase_order,
            'purchase_order_id': self._get_purchase_order_id,
            'questionnaire': self._get_questionnaire,
            'questionnaire_id': self._get_questionnaire_id,
            'questionnaire_access_method': self._get_questionnaire_access_method,
            'questionnaire_access_method_list': self._get_questionnaire_access_method_list,
            'questionnaire_questions': self._get_questionnaire_questions,
            'quote': self._get_quote,
            'quote_data': self._get_quote_data,
            'quote_directory': self._get_quote_directory,
            'quote_id': self._get_quote_id,
            'quote_pdf_filename': self._get_quote_pdf_filename,
            'quote_pdf_path': self._get_quote_pdf_path,
            'quote_proposal_pdf_filename': self._get_quote_proposal_pdf_filename,
            'quote_proposal_pdf_path': self._get_quote_proposal_pdf_path,
            'quote_total': self._get_quote_total,
            'quote_tax_amount': self._get_quote_tax_amount,
            'quote_subtotal': self._get_quote_subtotal,
            'taxes': self._get_taxes,
            'ready_date': self._get_ready_date,
            'reference_number': self._get_reference_number,
            'rush_order': self._get_rush_order,
            'sales_rep': self._get_sales_rep,
            'sales_rep_email': self._get_sales_rep_email,
            'sales_rep_id': self._get_sales_rep_id,
            'sales_rep_name': self._get_sales_rep_name,
            'shipment': self._get_shipment,
            'shipment_id': self._get_shipment_id,
            'shipment_method': self._get_shipping_method,
            'shipping_address': self._get_shipping_address,
            'shipping_city': self._get_shipping_city,
            'shipping_contact': self._get_shipping_contact,
            'shipping_contact_email': self._get_shipping_contact_email,
            'shipping_contact_firstname': self._get_shipping_contact_firstname,
            'shipping_contact_lastname': self._get_shipping_contact_lastname,
            'shipping_country': self._get_shipping_country,
            'shipping_google_link': self._get_shipping_google_link,
            'shipping_info': self._get_shipping_info,
            'shipping_location': self._get_shipping_location,
            'shipping_phone_number': self._get_shipping_phone_number,
            'shipping_postal_code': self._get_shipping_postal_code,
            'shipping_price': self._get_shipping_price,
            'shipping_price_ref': self._get_shipping_price_ref,
            'shipping_price_fast': self._get_shipping_price_fast,
            'shipping_province': self._get_shipping_province,
            'shipping_type': self._get_shipping_type,
            'shipping_type_method': self._get_shipping_type_method,
            'store': self._get_store,
            'store_image': self._get_store_image,
            'term_rows': self._get_term_rows,
            'term_values': self._get_term_values,
            'terms': self._get_terms,
            'terms_on_conversion': self._get_terms_on_conversion,
            'third_party_paint_pdf_filename': self._get_third_party_paint_pdf_filename,
            'third_party_paint_pdf_path': self._get_third_party_paint_pdf_path,
            'deficiency_report_pdf_filename': self._get_deficiency_report_pdf_filename,
            'deficiency_report_pdf_path': self._get_deficiency_report_pdf_path,
            'total': self._get_total,
            'work_sheet_pdf_filename': self._get_work_sheet_pdf_filename,
            'work_sheet_pdf_path': self._get_work_sheet_pdf_path,
            'invoice_pdf_filename': self._get_invoice_pdf_filename,
            'invoice_pdf_path': self._get_invoice_pdf_path,
            'invoice_id': self._get_invoice_id,
            'installer_booking': self._get_installer_booking,
            'installer': self._get_installer,
            'installer_company_name': self._get_installer_company_name,
            'installer_booking_installation_date': self._get_installer_booking_installation_date,
            'orders_pdf_filename': self._get_orders_pdf_filename,
            'orders_pdf_path': self._get_orders_pdf_path,

            # Product API Context
            'product_model': self._get_product_model,
            'product': self._get_product,
            'product_name': self._get_product_name,
            'product_price': self._get_product_price,
            'product_cost': self._get_product_cost,
            'product_weight': self._get_product_weight,
            'product_category': self._get_product_category,
            'product_description': self._get_product_description,
            'product_manufacturer': self._get_product_manufacturer,
            'product_mpn': self._get_product_mpn,
            'product_name_fr': self._get_product_name_fr,
            'product_description_fr': self._get_product_description_fr,
            'product_status': self._get_product_status,
            'product_created_at': self._get_product_created_at,
            'category_name': self._get_category_name,
            'category': self._get_category,
            'category_name_fr': self._get_category_name_fr,
            'category_description': self._get_category_description,
            'category_description_fr': self._get_category_description_fr,
            'category_parent': self._get_category_parent,
            'category_nav_bar': self._get_category_nav_bar,
            'category_status': self._get_category_status,
            'category_outside_paint': self._get_category_outside_paint,
            'category_cnc': self._get_category_cnc,
            'category_option_grp': self._get_category_option_grp,
            'category_image': self._get_category_image,
            'category_created_at': self._get_category_created_at,
            'category_updated_at': self._get_category_updated_at,
            'category_level_description': self._get_category_level_description,
            'category_three_model': self._get_category_three_model,
            'category_model_name': self._get_category_model_name,
            'category_overlapable': self._get_category_overlapable,
            'category_stackable': self._get_category_stackable,
            'category_stackontop': self._get_category_stackontop,
            'option_name': self._get_option_name,
            'option': self._get_option,
            'option_code': self._get_option_code,
            'option_description': self._get_option_description,
            'option_description_fr': self._get_option_description_fr,
            'option_manufacturer': self._get_option_manufacturer,
            'option_user_input': self._get_option_user_input,
            'option_price': self._get_option_price,
            'option_cost': self._get_option_cost,
            'option_image': self._get_option_image,
            'option_texture_height': self._get_option_texture_height,
            'option_texture_width': self._get_option_texture_width,
            'option_group_name': self._get_option_group_name,
            'option_group': self._get_option_group,
            'option_group_name_fr': self._get_option_group_name_fr,
            'option_group_description': self._get_option_group_description,
            'option_group_description_fr': self._get_option_group_description_fr,
            'option_group_default_option': self._get_option_group_default_option,
            'option_group_option': self._get_option_group_option,
            'option_group_image': self._get_option_group_image,
            'option_group_hide_show_model': self._get_option_group_hide_show_model,
            'option_group_option_margin': self._get_option_group_option_margin,
            'option_group_option_unit': self._get_option_group_option_unit,
            'option_group_base_cost': self._get_option_group_base_cost,
            'manufacturer_company_name': self._get_manufacturer_company_name,
            'manufacturer': self._get_manufacturer,
            'manufacturer_first_name': self._get_manufacturer_first_name,
            'manufacturer_last_name': self._get_manufacturer_last_name,
            'manufacturer_phone': self._get_manufacturer_phone,
            'manufacturer_email': self._get_manufacturer_email,
            'manufacturer_address': self._get_manufacturer_address,
            'manufacturer_city': self._get_manufacturer_city,
            'manufacturer_province': self._get_manufacturer_province,
            'manufacturer_postal_code': self._get_manufacturer_postal_code,
            'manufacturer_country': self._get_manufacturer_country,
            'manufacturer_currency': self._get_manufacturer_currency,
            'manufacturer_image': self._get_manufacturer_image,
            'manufacturer_purchase_method': self._get_manufacturer_purchase_method,
            'article_id': self._get_article_id,
            'article': self._get_article,
            'article_model': self._get_article_model,
            'article_options': self._get_article_options,
            'article_version': self._get_article_version,
            'article_compositions': self._get_article_compositions,
            'part_name': self._get_part_name,
            'part': self._get_part,
            'part_description': self._get_part_description,
            'part_mpn': self._get_part_mpn,
            'part_manufacturer': self._get_part_manufacturer,
            'part_units': self._get_part_units,
            'part_price': self._get_part_price,
            'part_standard_order': self._get_part_standard_order,
            'part_min_order': self._get_part_min_order,
            'part_image': self._get_part_image,
            'composition_id': self._get_composition_id,
            'composition': self._get_composition,
            'composition_list': self._get_composition_list,
            'composition_total': self._get_composition_total,
            'composition_article': self._get_composition_article,
            'composition_part': self._get_composition_part,
            'composition_quantity': self._get_composition_quantity,
            'purchase_orders_pdf_filename': self._get_purchase_orders_pdf_filename,
            'purchase_orders_pdf_path': self._get_purchase_orders_pdf_path,
            'materials_pdf_filename': self._get_materials_pdf_filename,
            'materials_pdf_path': self._get_materials_pdf_path,
            'address_map_image': self._get_address_map_image,
            'is_deficiency': self._get_is_deficiency,
        }

        self._context = {}
        self._fields = []

    def _get_is_deficiency(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)
    def _get_order_products_with_options(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_deficiency_items(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_purchase_orders_pdf_filename(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_purchase_orders_pdf_path(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_product_total(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_quote_tax_amount(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_quote_subtotal(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_taxes(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_proforma(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_proforma_id(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_purchase_order(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_purchase_order_id(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_orders_pdf_filename(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_orders_pdf_path(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_shipping_type_method(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_invoice_id(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_invoice(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_invoice_total(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_order_number(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_payments(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_payments_outstanding(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_payments_total(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_reference_number(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_sales_rep_name(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_shipping_price(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_shipping_price_ref(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_shipping_price_fast(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_term_rows(self):
        key = "term_rows"
        if key in self._context:
            return self._context[key]
        self._context[key] = len(self._get_term_values()) - list(self._get_term_values().values()).count([0.0, False])
        return self._context[key]

    def _get_term_values(self):
        if 'term_values' in self._context:
            return self._context['term_values']

        terms = self._get_terms()
        invoice = self._get_invoice()
        term_values = {"Order Confirmed": [
            (terms.on_order_conversion / 100) * float(invoice.total_with_tax),
            bool(invoice.proformainvoice_set.filter(invoice_stage='on_order_conversion').exists())],
            "Production Started": [(terms.on_production_commencing / 100) * float(invoice.total_with_tax), bool(
                invoice.proformainvoice_set.filter(invoice_stage='on_production_commencing').exists())],
            "Out For Delivery": [(terms.on_leaving_for_delivery / 100) * float(invoice.total_with_tax), bool(
                invoice.proformainvoice_set.filter(invoice_stage='on_leaving_for_delivery').exists())],
            "Installation Completed": [(terms.on_install_complete / 100) * float(invoice.total_with_tax), bool(
                invoice.proformainvoice_set.filter(invoice_stage='on_install_complete').exists())],
            "Order Completed": [(terms.on_order_completion / 100) * float(invoice.total_with_tax),
                                bool(
                                    invoice.proformainvoice_set.filter(invoice_stage='on_order_completion').exists())],
        }
        self._context['term_values'] = term_values
        return self._context['term_values']

    def set_base(self, base: object):
        """
        Used by model instances to avoid extra database call

        :type base: django model class
        set_base(self)
        """
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def api_connection(self, api, fields, ms):
        payload = self._api_payload(api, fields)
        data, status_code = ms().create("context", payload)
        if status_code == 200:
            for d in data:
                if d in self.values_map:
                    self._context[d] = data[d]
        return data, status_code

    def _api_payload(self, api, fields=None):
        # if fields is None:
        #     fields = []
        raise NotImplementedError("API connection not implemented " + sys._getframe().f_code.co_name)

    def get_context(self, value_list, context=None):
        if context is None:
            context = {}
        for value in value_list:
            if value in self.values_map:
                context[value] = self.values_map[value]()
            elif str(value).startswith("static_attachment"):
                def static_attachment():
                    item_name = str(value).strip()
                    if item_name not in self._context:
                        for i in range(2):
                            if item_name in self._context:
                                return self._context[item_name]
                            if i == 1:
                                # avoid extra http request
                                return []
                            # will assign self._context['project'] as a side effect
                            self.api_connection('order-api', [item_name], self._order_api)
                    return self._context[item_name]

                static_attachment.__name__ = str(value).strip()
                setattr(
                    self,
                    f"_get_{str(value).strip()}",
                    static_attachment
                )
                self.values_map[str(value).strip()] = getattr(self, f"_get_{str(value).strip()}")
                context[value] = self.values_map[value]()
        return context

    def context(self, static_values=None):
        if static_values is None:
            static_values = {}
        return self.get_context(self._fields, context=static_values)

    def get_value(self, value):
        if value in self.values_map:
            return self.values_map[value]()

        # dynamically createds a new method for the attatchment, and requests the data from the orders API
        # Order Api must overwrite static_attachment
        elif str(value).startswith("static_attachment"):
            def static_attachment():
                item_name = str(value).strip()
                if item_name not in self._context:
                    for i in range(2):
                        if item_name in self._context:
                            return self._context[item_name]
                        if i == 1:
                            # avoid extra http request
                            return []
                        # will assign self._context['project'] as a side effect
                        self.api_connection('order-api', [item_name], self._order_api)
                return self._context[item_name]

            static_attachment.__name__ = str(value).strip()
            setattr(
                self,
                f"_get_{str(value).strip()}",
                static_attachment
            )
            self.values_map[str(value).strip()] = getattr(self, f"_get_{str(value).strip()}")
            return self.values_map[value]()
        raise NotImplementedError(f"Could not find {value} in value map")

    def synonym(self, new, existing):
        if existing in self.values_map and new not in self.values_map:
            self.values_map[new] = self.values_map[existing]

    def synonyms(self, pairings: tuple):
        """
        :type pairings: (existing, new)
        """
        for pair in pairings:
            self.synonym(*pair)

    # debugging methods

    def _print_value_map(self):

        methods = {key[5:]: f"self.{key}" for key in dir(self) if key.startswith("_get_")}

        print("self.values_map = {")
        for k, v in methods.items():
            print(f"'{k}': {v},")
        print("}")

    def _print_abstract_func(self):
        func = [f"{key}" for key in dir(self) if key.startswith("_get_")]
        for m in func:
            print(f'{" " * 4}def {m}(self):\n'
                  f'{" " * 8}raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)\n')

    # implemented methods

    def _get_terms_on_conversion(self):
        item_name = 'terms_on_conversion'
        if item_name in self._context:
            return self._context[item_name]
        terms = self._get_terms()
        self._context[item_name] = terms.on_order_conversion
        return self._context[item_name]

    def _get_client_email(self):
        item_name = 'client_email'
        if item_name in self._context:
            return self._context[item_name]
        client = self._get_client()
        self._context[item_name] = client.email
        return self._context[item_name]

    def _get_business_legal_name(self):
        item_name = 'business_legal_name'
        if item_name in self._context:
            return self._context[item_name]
        account = self._get_account()
        self._context[item_name] = account.business_legal_name if account is not None else None
        return self._context[item_name]

    def _get_installer_payment_pickup(self):
        item_name = 'installer_payment_pickup'
        if item_name not in self._context:
            terms = self._get_terms()
            self._context[item_name] = bool(terms.on_install_complete)
        return self._context[item_name]

    def _get_company_address(self):
        item_name = 'company_address'
        if item_name in self._context:
            return self._context[item_name]
        self._context[item_name] = self._get_account().business_address
        return self._context[item_name]

    def _get_company_city(self):
        item_name = 'company_city'
        if item_name in self._context:
            return self._context[item_name]
        self._context[item_name] = self._get_account().business_city
        return self._context[item_name]

    def _get_company_name(self):
        item_name = 'company_name'
        if item_name in self._context:
            return self._context[item_name]
        self._context[item_name] = self._get_account().business_legal_name
        return self._context[item_name]

    def _get_company_postal_code(self):
        item_name = 'company_postal_code'
        if item_name in self._context:
            return self._context[item_name]
        self._context[item_name] = self._get_account().business_post_code.upper()
        return self._context[item_name]

    def _get_company_email(self):
        item_name = 'company_email'
        if item_name in self._context:
            return self._context[item_name]
        self._context[item_name] = self._get_account().business_email
        return self._context[item_name]

    def _get_store(self):
        item_name = 'store'
        if item_name in self._context:
            return self._context[item_name]
        account = self._get_account()
        self._context[item_name] = account.store
        return self._context[item_name]

    def _get_store_image(self):
        item_name = 'store_image'
        if item_name in self._context:
            return self._context[item_name]
        store = self._get_store()
        self._context[item_name] = store.signed_url()
        return self._context[item_name]

    def _get_account_group(self):
        item_name = 'account_group'
        if item_name in self._context:
            return self._context[item_name]
        account = self._get_account()
        self._context[item_name] = account.group
        return self._context[item_name]

    def _get_account_group_type(self):
        item_name = 'account_group_type'
        if item_name in self._context:
            return self._context[item_name]
        account = self._get_account_group()
        self._context[item_name] = account.type
        return self._context[item_name]

    # not implemented methods

    def _get_account(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_business_trade_name(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_client(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_client_cognito(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_client_name(self):
        if 'client_name' in self._context:
            return self._context['client_name']
        client = self._get_client()
        self._context['client_name'] = f"{client.first_name} {client.last_name}"
        return self._context['client_name']

    def _get_client_first_name(self):
        item_name = 'client_first_name'
        if item_name in self._context:
            return self._context[item_name]
        client = self._get_client()
        self._context[item_name] = client.first_name
        return self._context[item_name]

    def _get_client_last_name(self):
        item_name = 'client_last_name'
        if item_name in self._context:
            return self._context[item_name]
        client = self._get_client()
        self._context[item_name] = client.last_name
        return self._context[item_name]

    def _get_date(self):
        return datetime.now()

    def _get_cnc_items(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_delivery_questionnaire_hash(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_delivery_questionnaire_link(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_delivery_questionnaire_pdf_filename(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_delivery_questionnaire_pdf_path(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_extra_charges(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_fabric_coverage(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_fabric_calc(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_generated_path_files_folder(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_generated_path_installer_folder(self):
        item_name = "generated_installer_folder"
        if item_name in self._context:
            return self._context[item_name]
        gen_folder = self._get_generated_path_files_folder().rstrip('/').rstrip('\\')
        self._context[item_name] = rf"{gen_folder}/installers"
        return self._context[item_name]

    def _get_generated_path_installer_json(self):
        item_name = "generated_installer_json"
        if item_name in self._context:
            return self._context[item_name]
        folder = self._get_generated_path_installer_folder()
        self._context[item_name] = rf"{folder}/installer.json"
        return self._context[item_name]

    def _get_generated_path_installer_pdf(self):
        item_name = "generated_installer_pdf"
        if item_name in self._context:
            return self._context[item_name]
        folder = self._get_generated_path_installer_folder()
        self._context[item_name] = rf"{folder}/installer.pdf"
        return self._context[item_name]

    def _get_generated_path_shop_folder(self):
        item_name = "generated_shop_folder"
        if item_name in self._context:
            return self._context[item_name]
        gen_folder = self._get_generated_path_files_folder().rstrip('/').rstrip('\\')
        self._context[item_name] = rf"{gen_folder}/shop"
        return self._context[item_name]

    def _get_generated_path_shop_json(self):
        item_name = "generated_shop_json"
        if item_name in self._context:
            return self._context[item_name]
        folder = self._get_generated_path_shop_folder()
        self._context[item_name] = rf"{folder}/shop.json"
        return self._context[item_name]

    def _get_generated_path_shop_pdf(self):
        item_name = "generated_shop_pdf"
        if item_name in self._context:
            return self._context[item_name]
        folder = self._get_generated_path_shop_folder()
        self._context[item_name] = rf"{folder}/shop.pdf"
        return self._context[item_name]

    def _get_company_province(self):
        if 'company_province' in self._context:
            return self._context['company_province']
        self._context['company_province'] = self._get_account().business_state_province
        return self._context['company_province']

    def _get_group(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_quote_groups(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_job_title(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_lead_days(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_order(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_order_id(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_order_product(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_order_product_total(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_order_product_installed(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_order_products(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_outside_paint_products(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_packing_slip_pdf_filename(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_packing_slip_pdf_path(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_products(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_project(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_project_directory(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_project_id(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_questionnaire(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_questionnaire_id(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_questionnaire_access_method(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_questionnaire_access_method_list(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_questionnaire_questions(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_quote(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_quote_data(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_quote_total(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_quote_directory(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_quote_id(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_quote_pdf_filename(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_quote_pdf_path(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_quote_proposal_pdf_filename(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_quote_proposal_pdf_path(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_ready_date(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_rush_order(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_sales_rep(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_sales_rep_email(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_sales_rep_id(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_shipment(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_shipment_id(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_pretax(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_shipping_address(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_shipping_city(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_shipping_contact(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_shipping_contact_email(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_shipping_contact_firstname(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_shipping_contact_lastname(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_shipping_country(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_shipping_google_link(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_shipping_info(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_shipping_location(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_shipping_method(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_shipping_phone_number(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_shipping_postal_code(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_shipping_province(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_shipping_type(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_terms(self):
        if 'terms' in self._context:
            return self._context['terms']
        self._context['terms'] = self._get_account().payment_terms
        return self._context['terms']

    def _get_third_party_paint_pdf_filename(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_third_party_paint_pdf_path(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_deficiency_report_pdf_filename(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_deficiency_report_pdf_path(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_invoice_pdf_filename(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_invoice_pdf_path(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_total(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_work_order_pdf_filename(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_work_order_pdf_path(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_work_sheet_pdf_filename(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_work_sheet_pdf_path(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_installer_booking(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_installer(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_installer_company_name(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_installer_booking_installation_date(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def get_all(self, context=None):

        if context is None:
            context = {}
        for key, value in self.values_map.items():
            try:
                context[key] = self.values_map[key]()
            except NotImplementedError as e:
                print(e)

        return context

    def _get_blank_checkbox(self):
        item_name = "blank_checkbox"
        if item_name in self._context:
            return self._context[item_name]
        key = "images/blank_checkbox.png"
        self._context[item_name] = ResourcesStorage().signed_url(key)
        return self._context[item_name]

    def _get_checkbox(self):
        item_name = "checkbox"
        if item_name in self._context:
            return self._context[item_name]
        key = "images/checkbox.png"
        self._context[item_name] = ResourcesStorage().signed_url(key)
        return self._context[item_name]

    def required_contexts(self, template_path, render_engine):
        all_fields = self.get_all()
        original_result = render_engine(template_path, all_fields)
        fields = [(field, True) for field in all_fields.keys()]
        for index in range(len(fields)):
            copy_fields = copy.deepcopy(all_fields)
            field = fields[index][0]
            del copy_fields[field]
            new_result = render_engine(template_path, copy_fields)
            if new_result == original_result:
                fields[index] = (field, False)

        for field in fields:
            if field[1] is False:
                del all_fields[field[0]]
        return list(all_fields.keys())

    # Product API Functions

    def _get_product_model(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_product(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_product_name(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_product_price(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_product_cost(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_product_weight(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_product_category(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_product_description(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_product_manufacturer(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_product_mpn(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_product_name_fr(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_product_description_fr(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_product_status(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_product_created_at(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_category_name(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_category(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_category_name_fr(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_category_description(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_category_description_fr(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_category_parent(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_category_nav_bar(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_category_status(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_category_outside_paint(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_category_cnc(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_category_option_grp(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_category_image(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_category_created_at(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_category_updated_at(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_category_level_description(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_category_three_model(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_category_model_name(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_category_overlapable(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_category_stackable(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_category_stackontop(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_option_name(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_option(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_option_code(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_option_description(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_option_description_fr(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_option_manufacturer(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_option_user_input(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_option_price(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_option_cost(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_option_image(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_option_texture_height(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_option_texture_width(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_option_group_name(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_option_group(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_option_group_name_fr(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_option_group_description(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_option_group_description_fr(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_option_group_default_option(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_option_group_option(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_option_group_image(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_option_group_hide_show_model(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_option_group_option_margin(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_option_group_option_unit(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_option_group_base_cost(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_manufacturer_company_name(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_manufacturer(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_manufacturer_first_name(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_manufacturer_last_name(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_manufacturer_phone(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_manufacturer_email(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_manufacturer_address(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_manufacturer_city(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_manufacturer_province(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_manufacturer_postal_code(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_manufacturer_country(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_manufacturer_currency(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_manufacturer_image(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_manufacturer_purchase_method(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_article_id(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_article(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_article_model(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_article_options(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_article_version(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_article_compositions(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_part_name(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_part(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_part_description(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_part_mpn(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_part_manufacturer(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_part_units(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_part_price(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_part_standard_order(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_part_min_order(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_part_image(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_composition_id(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_composition(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_composition_list(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_composition_total(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_composition_article(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_composition_part(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_composition_quantity(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_materials_pdf_filename(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_materials_pdf_path(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_address_map_image(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_cnc_data(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_deficiency_item(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_cutlist_quotes(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_cutlist_deficiencies(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_cutlist_orders(self):
        raise NotImplementedError("Method not implemented " + sys._getframe().f_code.co_name)

    def _get_customer_po(self):
        item_name = "customer_po"
        if item_name not in self._context:
            project = self._get_project()
            self._context[item_name] = project.customer_po
        return self._context[item_name]
