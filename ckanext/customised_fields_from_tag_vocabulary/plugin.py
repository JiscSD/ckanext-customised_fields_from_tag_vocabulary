from __future__ import annotations

from ckan.common import CKANConfig
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import logging
import json

from flask import render_template
from ckan.plugins.toolkit import Invalid

log = logging.getLogger(__name__)
facet_order_by_display_name = ['Year']

def get_vocab_tag_list(vocab):
    try:
        vocab_list = toolkit.get_action('vocabulary_show')
        result_list = vocab_list(data_dict={'id': vocab})

        agg_list = {}
        for rr in result_list['tags']:
            agg_list[rr['id']] = rr['name']

        return agg_list.items()
    except toolkit.ObjectNotFound:
        return None

def reorder_facet(title, facet):
    if title in facet_order_by_display_name:
        sfacet = sorted(facet, key=lambda d: d['display_name'], reverse=True)
        return sfacet 
    return facet

class CustomisedFieldsFromTagVocabularyPlugin(plugins.SingletonPlugin, toolkit.DefaultDatasetForm):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IDatasetForm)
    plugins.implements(plugins.IFacets)
    plugins.implements(plugins.IPackageController)

    # IFacets  (side filters)

    def dataset_facets(self, facets_dict, package_type):

        facets_dict['vocab_Year'] = plugins.toolkit._(u'Year')
        facets_dict['vocab_Topics'] = plugins.toolkit._(u'Topics')
        facets_dict['vocab_Unit'] = plugins.toolkit._(u'Unit')
        facets_dict["vocab_Area_type"] = plugins.toolkit._(u'Area Type')
        del facets_dict['groups']

        return facets_dict

    def group_facets(self, facets_dict, group_type, package_type):
        
        return facets_dict

    def organization_facets(self, facets_dict, organization_type, package_type):
        
        return facets_dict

    # IPackageController
    def read(self, entity):
        pass

    def create(self, entity):
        pass

    def edit(self, entity):
        pass

    def authz_add_role(self, object_role):
        pass

    def authz_remove_role(self, object_role):
        pass

    def delete(self, entity):
        pass

    def before_search(self, search_params):
        return search_params

    def after_search(self, search_results, search_params):
        return search_results

    def before_index(self, data_dict):
        data_dict.pop('wkt', None)
        data_dict.pop('extras_wkt', None)
        return data_dict

    def before_view(self, pkg_dict):
        return pkg_dict

    def after_create(self, context, data_dict):
        return data_dict

    def after_update(self, context, data_dict):
        return data_dict

    def after_delete(self, context, data_dict):
        return data_dict

    def after_show(self, context, data_dict):
        return data_dict

    # IConfigurer

    def update_config(self, _config):
        toolkit.add_template_directory(_config, 'templates')
        toolkit.add_public_directory(_config, 'public')
        toolkit.add_resource('fanstatic',
            'customised_fields_from_tag_vocabulary')

    # ITemplateHelpers

    def get_helpers(self):
        return {'get_vocab_tag_list': get_vocab_tag_list, 'reorder_facet': reorder_facet}

    def is_fallback(self):
        # Return True to register this plugin as the default handler for
        # package types not handled by any other IDatasetForm plugin.
        return True

    def package_types(self) -> list[str]:
        # This plugin doesn't handle any special package types, it just
        # registers itself as the default (above).
        return []

    # IDatasetForm

    def _modify_package_schema(self, schema: Schema):
        # Add our custom year metadata field to the schema.
        schema.update({
                'years': [
                    toolkit.get_validator('ignore_missing'),
                    toolkit.get_converter('convert_to_tags')('Year')]
                })

        schema.update({
                'topics': [
                    toolkit.get_validator('ignore_missing'),
                    toolkit.get_converter('convert_to_tags')('Topics')]
                })

        schema.update({
                'units': [
                    toolkit.get_validator('ignore_missing'),
                    toolkit.get_converter('convert_to_tags')('Unit')]
                })

        schema.update({
                'area_types': [
                    toolkit.get_validator('ignore_missing'),
                    toolkit.get_converter('convert_to_tags')('Area_type')]
                })

        schema.update({
                'frequency': [
                    toolkit.get_validator('ignore_missing'),
                    toolkit.get_converter('convert_to_tags')('Frequency')]
                })

        schema.update({
                'doi': [
                    toolkit.get_validator('ignore_missing'),
                    toolkit.get_converter('convert_to_extras')]
                })

        schema.update({
                'citation': [
                    toolkit.get_validator('ignore_missing'),
                    toolkit.get_converter('convert_to_extras')]
                })

        schema.update({
                'geographic_coverage': [
                    toolkit.get_validator('ignore_missing'),
                    toolkit.get_converter('convert_to_extras')]
                })

        schema.update({
                'granularity': [
                    toolkit.get_validator('ignore_missing'),
                    toolkit.get_converter('convert_to_extras')]
                })

        schema.update({
                'geographic_spatial': [
                    toolkit.get_validator('ignore_missing'),
                    toolkit.get_converter('convert_to_extras')]
                })

        schema.update({
                'wkt': [
                    toolkit.get_validator('ignore_missing'),
                    toolkit.get_converter('convert_to_extras')]
                })

        
        return schema

    def create_package_schema(self):
        schema = super(CustomisedFieldsFromTagVocabularyPlugin, self).create_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

    def update_package_schema(self):
        schema = super(CustomisedFieldsFromTagVocabularyPlugin, self).update_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

    def show_package_schema(self) -> Schema:
        schema = super(CustomisedFieldsFromTagVocabularyPlugin, self).show_package_schema()
        schema.update({
            'doi': [toolkit.get_converter('convert_from_extras'),
                            toolkit.get_validator('ignore_missing')]
        })
        schema.update({
            'citation': [toolkit.get_converter('convert_from_extras'),
                            toolkit.get_validator('ignore_missing')]
        })
        schema.update({
            'geographic_coverage': [toolkit.get_converter('convert_from_extras'),
                            toolkit.get_validator('ignore_missing')]
        })
        schema.update({
            'granularity': [toolkit.get_converter('convert_from_extras'),
                            toolkit.get_validator('ignore_missing')]
        })
        schema.update({
            'geographic_spatial': [toolkit.get_converter('convert_from_extras'),
                            toolkit.get_validator('ignore_missing')]
        })
        schema.update({
            'wkt': [toolkit.get_converter('convert_from_extras'),
                            toolkit.get_validator('ignore_missing')]
        })

        schema['tags']['__extras'].append(toolkit.get_converter('free_tags_only'))
        schema.update({
            'years': [
                toolkit.get_converter('convert_from_tags')('Year'),
                toolkit.get_validator('ignore_missing')]
        })
        schema.update({
            'topics': [
                toolkit.get_converter('convert_from_tags')('Topics'),
                toolkit.get_validator('ignore_missing')]
        })
        schema.update({
            'units': [
                toolkit.get_converter('convert_from_tags')('Unit'),
                toolkit.get_validator('ignore_missing')]
        })
        schema.update({
            'area_types': [
                toolkit.get_converter('convert_from_tags')('Area_type'),
                toolkit.get_validator('ignore_missing')]
        })
        schema.update({
            'frequency': [
                toolkit.get_converter('convert_from_tags')('Frequency'),
                toolkit.get_validator('ignore_missing')]
        })
        return schema