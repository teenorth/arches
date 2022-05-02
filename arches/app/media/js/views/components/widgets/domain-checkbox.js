define([
    'knockout',
    'viewmodels/domain-widget',
    'utils/create-async-component',
    'plugins/knockout-select2',
    'templates/views/components/widgets/checkbox.htm'
], function(ko, DomainWidgetViewModel, createAsyncComponent) {
    /**
     * registers a select-widget component for use in forms
     * @function external:"ko.components".select-widget
     * @param {object} params
     * @param {boolean} params.value - the value being managed
     * @param {object} params.config -
     * @param {string} params.config.label - label to use alongside the select input
     * @param {string} params.config.placeholder - default text to show in the select input
     * @param {string} params.config.options -
     */
    
    const viewModel = function(params) {
        params.configKeys = ['defaultValue'];
        DomainWidgetViewModel.apply(this, [params]);

        this.multiple = true;
    };

    return createAsyncComponent(
        'domain-checkbox-widget',
        viewModel,
        'templates/views/components/widgets/checkbox.htm'
    );
});
