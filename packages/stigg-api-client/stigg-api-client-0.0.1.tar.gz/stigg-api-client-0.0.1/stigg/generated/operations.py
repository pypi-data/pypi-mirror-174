import sgqlc.types
import sgqlc.operation
from . import schema

_schema = schema
_schema_root = _schema.schema

__all__ = ('Operations',)


def fragment_plan_fragment():
    _frag = sgqlc.operation.Fragment(_schema.Plan, 'PlanFragment')
    _frag.ref_id(__alias__='id')
    _frag.display_name()
    _frag.description()
    _frag.additional_meta_data(__alias__='metadata')
    _frag_product = _frag.product()
    _frag_product.ref_id(__alias__='id')
    _frag_product.display_name()
    _frag_product.description()
    _frag_base_plan = _frag.base_plan()
    _frag_base_plan.ref_id(__alias__='id')
    _frag_base_plan.display_name()
    _frag_entitlements = _frag.entitlements()
    _frag_entitlements.__fragment__(fragment_package_entitlement_fragment())
    _frag_inherited_entitlements = _frag.inherited_entitlements()
    _frag_inherited_entitlements.__fragment__(fragment_package_entitlement_fragment())
    _frag_compatible_addons = _frag.compatible_addons()
    _frag_compatible_addons.__fragment__(fragment_addon_fragment())
    _frag_prices = _frag.prices()
    _frag_prices.__fragment__(fragment_price_fragment())
    _frag.pricing_type()
    _frag_default_trial_config = _frag.default_trial_config()
    _frag_default_trial_config.duration()
    _frag_default_trial_config.units()
    return _frag


def fragment_total_price_fragment():
    _frag = sgqlc.operation.Fragment(_schema.CustomerSubscriptionTotalPrice, 'TotalPriceFragment')
    _frag_sub_total = _frag.sub_total()
    _frag_sub_total.amount()
    _frag_sub_total.currency()
    _frag_total = _frag.total()
    _frag_total.amount()
    _frag_total.currency()
    return _frag


def fragment_price_fragment():
    _frag = sgqlc.operation.Fragment(_schema.Price, 'PriceFragment')
    _frag.billing_model()
    _frag.billing_period()
    _frag_price = _frag.price()
    _frag_price.amount()
    _frag_price.currency()
    _frag_feature = _frag.feature()
    _frag_feature.__fragment__(fragment_feature_fragment())
    return _frag


def fragment_package_entitlement_fragment():
    _frag = sgqlc.operation.Fragment(_schema.PackageEntitlement, 'PackageEntitlementFragment')
    _frag.usage_limit()
    _frag.has_unlimited_usage()
    _frag.feature_id()
    _frag.reset_period()
    _frag_feature = _frag.feature()
    _frag_feature.__fragment__(fragment_feature_fragment())
    return _frag


def fragment_addon_fragment():
    _frag = sgqlc.operation.Fragment(_schema.Addon, 'AddonFragment')
    _frag.ref_id(__alias__='id')
    _frag.display_name()
    _frag.description()
    _frag.additional_meta_data(__alias__='metadata')
    _frag_entitlements = _frag.entitlements()
    _frag_entitlements.__fragment__(fragment_package_entitlement_fragment())
    _frag.pricing_type()
    return _frag


def fragment_subscription_fragment():
    _frag = sgqlc.operation.Fragment(_schema.CustomerSubscription, 'SubscriptionFragment')
    _frag.ref_id(__alias__='id')
    _frag.status()
    _frag.start_date()
    _frag.end_date()
    _frag.trial_end_date()
    _frag.cancellation_date()
    _frag.effective_end_date()
    _frag.current_billing_period_end()
    _frag.additional_meta_data(__alias__='metadata')
    _frag.billing_id()
    _frag.billing_link_url()
    _frag_prices = _frag.prices()
    _frag_prices.usage_limit()
    _frag_prices_price = _frag_prices.price()
    _frag_prices_price.__fragment__(fragment_price_fragment())
    _frag_total_price = _frag.total_price()
    _frag_total_price.__fragment__(fragment_total_price_fragment())
    _frag.pricing_type()
    _frag_plan = _frag.plan()
    _frag_plan.__fragment__(fragment_plan_fragment())
    _frag_addons = _frag.addons()
    _frag_addons.id()
    _frag_addons.quantity()
    _frag_addons_addon = _frag_addons.addon()
    _frag_addons_addon.__fragment__(fragment_addon_fragment())
    return _frag


def fragment_promotional_entitlement_fragment():
    _frag = sgqlc.operation.Fragment(_schema.PromotionalEntitlement, 'PromotionalEntitlementFragment')
    _frag.status()
    _frag.usage_limit()
    _frag.feature_id()
    _frag.has_unlimited_usage()
    _frag.reset_period()
    _frag.end_date()
    _frag.is_visible()
    _frag_feature = _frag.feature()
    _frag_feature.__fragment__(fragment_feature_fragment())
    return _frag


def fragment_coupon_fragment():
    _frag = sgqlc.operation.Fragment(_schema.Coupon, 'CouponFragment')
    _frag.ref_id(__alias__='id')
    _frag.name()
    _frag.description()
    _frag.type()
    _frag.discount_value()
    _frag.additional_meta_data(__alias__='metadata')
    _frag.created_at()
    _frag.updated_at()
    _frag.billing_id()
    _frag.billing_link_url()
    _frag.status()
    return _frag


def fragment_customer_fragment():
    _frag = sgqlc.operation.Fragment(_schema.Customer, 'CustomerFragment')
    _frag.ref_id(__alias__='id')
    _frag.name()
    _frag.email()
    _frag.created_at()
    _frag.updated_at()
    _frag_subscriptions = _frag.subscriptions()
    _frag_subscriptions.__fragment__(fragment_subscription_fragment())
    _frag_promotional_entitlements = _frag.promotional_entitlements()
    _frag_promotional_entitlements.__fragment__(fragment_promotional_entitlement_fragment())
    _frag.has_payment_method()
    _frag_coupon = _frag.coupon()
    _frag_coupon.__fragment__(fragment_coupon_fragment())
    _frag.billing_id()
    _frag.additional_meta_data(__alias__='metadata')
    return _frag


def fragment_slim_subscription_fragment():
    _frag = sgqlc.operation.Fragment(_schema.CustomerSubscription, 'SlimSubscriptionFragment')
    _frag.ref_id(__alias__='id')
    _frag.status()
    _frag.additional_meta_data(__alias__='metadata')
    _frag.billing_id()
    _frag.billing_link_url()
    _frag.effective_end_date()
    _frag.current_billing_period_end()
    _frag.pricing_type()
    _frag_prices = _frag.prices()
    _frag_prices.usage_limit()
    _frag_prices_price = _frag_prices.price()
    _frag_prices_price.__fragment__(fragment_price_fragment())
    _frag_total_price = _frag.total_price()
    _frag_total_price.__fragment__(fragment_total_price_fragment())
    _frag_plan = _frag.plan()
    _frag_plan.ref_id(__alias__='id')
    _frag_addons = _frag.addons()
    _frag_addons.quantity()
    _frag_addons_addon = _frag_addons.addon()
    _frag_addons_addon.ref_id(__alias__='id')
    _frag_customer = _frag.customer()
    _frag_customer.ref_id(__alias__='id')
    return _frag


def fragment_paywall_plan_fragment():
    _frag = sgqlc.operation.Fragment(_schema.Plan, 'PaywallPlanFragment')
    _frag.ref_id(__alias__='id')
    _frag.description()
    _frag.display_name()
    _frag_product = _frag.product()
    _frag_product.ref_id(__alias__='id')
    _frag_product.display_name()
    _frag_product.description()
    _frag_base_plan = _frag.base_plan()
    _frag_base_plan.ref_id(__alias__='id')
    _frag_base_plan.display_name()
    _frag_entitlements = _frag.entitlements()
    _frag_entitlements.__fragment__(fragment_paywall_package_entitlement_fragment())
    _frag.additional_meta_data(__alias__='metadata')
    _frag_inherited_entitlements = _frag.inherited_entitlements()
    _frag_inherited_entitlements.__fragment__(fragment_paywall_package_entitlement_fragment())
    _frag_prices = _frag.prices()
    _frag_prices.__fragment__(fragment_paywall_price_fragment())
    _frag.pricing_type()
    _frag_default_trial_config = _frag.default_trial_config()
    _frag_default_trial_config.duration()
    _frag_default_trial_config.units()
    return _frag


def fragment_feature_fragment():
    _frag = sgqlc.operation.Fragment(_schema.Feature, 'FeatureFragment')
    _frag.ref_id(__alias__='id')
    _frag.feature_type()
    _frag.meter_type()
    _frag.feature_units()
    _frag.feature_units_plural()
    _frag.display_name()
    _frag.description()
    return _frag


def fragment_entitlement_feature_fragment():
    _frag = sgqlc.operation.Fragment(_schema.EntitlementFeature, 'EntitlementFeatureFragment')
    _frag.ref_id(__alias__='id')
    _frag.feature_type()
    _frag.meter_type()
    _frag.feature_units()
    _frag.feature_units_plural()
    _frag.display_name()
    _frag.description()
    return _frag


def fragment_paywall_package_entitlement_fragment():
    _frag = sgqlc.operation.Fragment(_schema.PackageEntitlement, 'PaywallPackageEntitlementFragment')
    _frag.usage_limit()
    _frag.has_unlimited_usage()
    _frag.feature_id()
    _frag.reset_period()
    _frag_feature = _frag.feature()
    _frag_feature.__fragment__(fragment_feature_fragment())
    return _frag


def fragment_paywall_price_fragment():
    _frag = sgqlc.operation.Fragment(_schema.Price, 'PaywallPriceFragment')
    _frag.billing_model()
    _frag.billing_period()
    _frag_price = _frag.price()
    _frag_price.amount()
    _frag_price.currency()
    _frag_feature = _frag.feature()
    _frag_feature.__fragment__(fragment_feature_fragment())
    return _frag


def fragment_paywall_addon_fragment():
    _frag = sgqlc.operation.Fragment(_schema.Addon, 'PaywallAddonFragment')
    _frag.ref_id(__alias__='id')
    _frag.display_name()
    _frag.description()
    _frag_entitlements = _frag.entitlements()
    _frag_entitlements.__fragment__(fragment_paywall_package_entitlement_fragment())
    _frag_prices = _frag.prices()
    _frag_prices.__fragment__(fragment_paywall_price_fragment())
    _frag.additional_meta_data(__alias__='metadata')
    _frag.pricing_type()
    return _frag


def fragment_subscription_preview_fragment():
    _frag = sgqlc.operation.Fragment(_schema.SubscriptionPreview, 'SubscriptionPreviewFragment')
    _frag_sub_total = _frag.sub_total()
    _frag_sub_total.amount()
    _frag_sub_total.currency()
    _frag_total = _frag.total()
    _frag_total.amount()
    _frag_total.currency()
    _frag_billing_period_range = _frag.billing_period_range()
    _frag_billing_period_range.start()
    _frag_billing_period_range.end()
    _frag_proration = _frag.proration()
    _frag_proration.proration_date()
    _frag_proration_credit = _frag_proration.credit()
    _frag_proration_credit.amount()
    _frag_proration_credit.currency()
    _frag_proration_debit = _frag_proration.debit()
    _frag_proration_debit.amount()
    _frag_proration_debit.currency()
    return _frag


def fragment_entitlement_fragment():
    _frag = sgqlc.operation.Fragment(_schema.Entitlement, 'EntitlementFragment')
    _frag.is_granted()
    _frag.access_denied_reason()
    _frag.customer_id()
    _frag.usage_limit()
    _frag.has_unlimited_usage()
    _frag.current_usage()
    _frag.requested_usage()
    _frag.next_reset_date()
    _frag.reset_period()
    _frag_reset_period_configuration = _frag.reset_period_configuration()
    _frag_reset_period_configuration.__fragment__(fragment_reset_period_configuration_fragment())
    _frag_feature = _frag.feature()
    _frag_feature.__fragment__(fragment_entitlement_feature_fragment())
    return _frag


def fragment_reset_period_configuration_fragment():
    _frag = sgqlc.operation.Fragment(_schema.ResetPeriodConfiguration, 'ResetPeriodConfigurationFragment')
    _frag__as__MonthlyResetPeriodConfig = _frag.__as__(_schema.MonthlyResetPeriodConfig)
    _frag__as__MonthlyResetPeriodConfig.__fragment__(fragment_monthly_reset_period_config_fragment())
    _frag__as__WeeklyResetPeriodConfig = _frag.__as__(_schema.WeeklyResetPeriodConfig)
    _frag__as__WeeklyResetPeriodConfig.__fragment__(fragment_weekly_reset_period_config_fragment())
    return _frag


def fragment_monthly_reset_period_config_fragment():
    _frag = sgqlc.operation.Fragment(_schema.MonthlyResetPeriodConfig, 'MonthlyResetPeriodConfigFragment')
    _frag.monthly_according_to()
    return _frag


def fragment_weekly_reset_period_config_fragment():
    _frag = sgqlc.operation.Fragment(_schema.WeeklyResetPeriodConfig, 'WeeklyResetPeriodConfigFragment')
    _frag.weekly_according_to()
    return _frag


class Fragment:
    addon_fragment = fragment_addon_fragment()
    coupon_fragment = fragment_coupon_fragment()
    customer_fragment = fragment_customer_fragment()
    entitlement_feature_fragment = fragment_entitlement_feature_fragment()
    entitlement_fragment = fragment_entitlement_fragment()
    feature_fragment = fragment_feature_fragment()
    monthly_reset_period_config_fragment = fragment_monthly_reset_period_config_fragment()
    package_entitlement_fragment = fragment_package_entitlement_fragment()
    paywall_addon_fragment = fragment_paywall_addon_fragment()
    paywall_package_entitlement_fragment = fragment_paywall_package_entitlement_fragment()
    paywall_plan_fragment = fragment_paywall_plan_fragment()
    paywall_price_fragment = fragment_paywall_price_fragment()
    plan_fragment = fragment_plan_fragment()
    price_fragment = fragment_price_fragment()
    promotional_entitlement_fragment = fragment_promotional_entitlement_fragment()
    reset_period_configuration_fragment = fragment_reset_period_configuration_fragment()
    slim_subscription_fragment = fragment_slim_subscription_fragment()
    subscription_fragment = fragment_subscription_fragment()
    subscription_preview_fragment = fragment_subscription_preview_fragment()
    total_price_fragment = fragment_total_price_fragment()
    weekly_reset_period_config_fragment = fragment_weekly_reset_period_config_fragment()


def mutation_create_customer():
    _op = sgqlc.operation.Operation(_schema_root.mutation_type, name='createCustomer', variables=dict(input=sgqlc.types.Arg(sgqlc.types.non_null(_schema.CustomerInput))))
    _op_create_customer = _op.create_one_customer(input=sgqlc.types.Variable('input'), __alias__='create_customer')
    _op_create_customer.__fragment__(fragment_customer_fragment())
    return _op


def mutation_provision_customer():
    _op = sgqlc.operation.Operation(_schema_root.mutation_type, name='provisionCustomer', variables=dict(input=sgqlc.types.Arg(sgqlc.types.non_null(_schema.ProvisionCustomerInput))))
    _op_provision_customer = _op.provision_customer(input=sgqlc.types.Variable('input'))
    _op_provision_customer_customer = _op_provision_customer.customer()
    _op_provision_customer_customer.__fragment__(fragment_customer_fragment())
    _op_provision_customer.subscription_strategy_decision()
    _op_provision_customer_subscription = _op_provision_customer.subscription()
    _op_provision_customer_subscription.__fragment__(fragment_slim_subscription_fragment())
    return _op


def mutation_import_customer():
    _op = sgqlc.operation.Operation(_schema_root.mutation_type, name='importCustomer', variables=dict(input=sgqlc.types.Arg(sgqlc.types.non_null(_schema.ImportCustomerInput))))
    _op_import_customer = _op.import_one_customer(input=sgqlc.types.Variable('input'), __alias__='import_customer')
    _op_import_customer.__fragment__(fragment_customer_fragment())
    return _op


def mutation_update_customer():
    _op = sgqlc.operation.Operation(_schema_root.mutation_type, name='updateCustomer', variables=dict(input=sgqlc.types.Arg(sgqlc.types.non_null(_schema.UpdateCustomerInput))))
    _op_update_customer = _op.update_one_customer(input=sgqlc.types.Variable('input'), __alias__='update_customer')
    _op_update_customer.__fragment__(fragment_customer_fragment())
    return _op


def mutation_update_subscription():
    _op = sgqlc.operation.Operation(_schema_root.mutation_type, name='updateSubscription', variables=dict(input=sgqlc.types.Arg(sgqlc.types.non_null(_schema.UpdateSubscriptionInput))))
    _op_update_subscription = _op.update_one_subscription(input=sgqlc.types.Variable('input'), __alias__='update_subscription')
    _op_update_subscription.__fragment__(fragment_slim_subscription_fragment())
    return _op


def mutation_create_subscription():
    _op = sgqlc.operation.Operation(_schema_root.mutation_type, name='createSubscription', variables=dict(input=sgqlc.types.Arg(sgqlc.types.non_null(_schema.SubscriptionInput))))
    _op_create_subscription = _op.create_subscription(subscription=sgqlc.types.Variable('input'))
    _op_create_subscription.__fragment__(fragment_slim_subscription_fragment())
    return _op


def mutation_cancel_subscription():
    _op = sgqlc.operation.Operation(_schema_root.mutation_type, name='cancelSubscription', variables=dict(input=sgqlc.types.Arg(sgqlc.types.non_null(_schema.SubscriptionCancellationInput))))
    _op_cancel_subscription = _op.cancel_subscription(input=sgqlc.types.Variable('input'))
    _op_cancel_subscription.__fragment__(fragment_slim_subscription_fragment())
    return _op


def mutation_initiate_checkout():
    _op = sgqlc.operation.Operation(_schema_root.mutation_type, name='initiateCheckout', variables=dict(input=sgqlc.types.Arg(sgqlc.types.non_null(_schema.InitiateCheckoutInput))))
    _op_initiate_checkout = _op.initiate_checkout(input=sgqlc.types.Variable('input'))
    _op_initiate_checkout.id()
    _op_initiate_checkout.checkout_url()
    _op_initiate_checkout.checkout_billing_id()
    return _op


def mutation_estimate_subscription():
    _op = sgqlc.operation.Operation(_schema_root.mutation_type, name='EstimateSubscription', variables=dict(input=sgqlc.types.Arg(sgqlc.types.non_null(_schema.EstimateSubscriptionInput))))
    _op_estimate_subscription = _op.estimate_subscription(input=sgqlc.types.Variable('input'))
    _op_estimate_subscription.__fragment__(fragment_subscription_preview_fragment())
    return _op


def mutation_estimate_subscription_update():
    _op = sgqlc.operation.Operation(_schema_root.mutation_type, name='EstimateSubscriptionUpdate', variables=dict(input=sgqlc.types.Arg(sgqlc.types.non_null(_schema.EstimateSubscriptionUpdateInput))))
    _op_estimate_subscription_update = _op.estimate_subscription_update(input=sgqlc.types.Variable('input'))
    _op_estimate_subscription_update.__fragment__(fragment_subscription_preview_fragment())
    return _op


def mutation_create_usage_measurement():
    _op = sgqlc.operation.Operation(_schema_root.mutation_type, name='CreateUsageMeasurement', variables=dict(input=sgqlc.types.Arg(sgqlc.types.non_null(_schema.UsageMeasurementCreateInput))))
    _op_create_usage_measurement = _op.create_usage_measurement(usage_measurement=sgqlc.types.Variable('input'))
    _op_create_usage_measurement.id()
    return _op


class Mutation:
    cancel_subscription = mutation_cancel_subscription()
    create_customer = mutation_create_customer()
    create_subscription = mutation_create_subscription()
    create_usage_measurement = mutation_create_usage_measurement()
    estimate_subscription = mutation_estimate_subscription()
    estimate_subscription_update = mutation_estimate_subscription_update()
    import_customer = mutation_import_customer()
    initiate_checkout = mutation_initiate_checkout()
    provision_customer = mutation_provision_customer()
    update_customer = mutation_update_customer()
    update_subscription = mutation_update_subscription()


def query_get_customer_by_id():
    _op = sgqlc.operation.Operation(_schema_root.query_type, name='getCustomerById', variables=dict(customerId=sgqlc.types.Arg(_schema.String)))
    _op_customers = _op.customers(filter={'refId': {'eq': sgqlc.types.Variable('customerId')}})
    _op_customers_edges = _op_customers.edges()
    _op_customers_edges_node = _op_customers_edges.node()
    _op_customers_edges_node.__fragment__(fragment_customer_fragment())
    return _op


def query_get_coupons():
    _op = sgqlc.operation.Operation(_schema_root.query_type, name='getCoupons')
    _op_coupons = _op.coupons(filter={'status': {'eq': 'ACTIVE'}}, paging={'first': 50})
    _op_coupons_edges = _op_coupons.edges()
    _op_coupons_edges_node = _op_coupons_edges.node()
    _op_coupons_edges_node.__fragment__(fragment_coupon_fragment())
    return _op


def query_get_paywall():
    _op = sgqlc.operation.Operation(_schema_root.query_type, name='GetPaywall', variables=dict(input=sgqlc.types.Arg(sgqlc.types.non_null(_schema.GetPaywallInput))))
    _op_get_paywall = _op.get_paywall(input=sgqlc.types.Variable('input'))
    _op_get_paywall.__fragment__(fragment_paywall_plan_fragment())
    return _op


def query_entitlements():
    _op = sgqlc.operation.Operation(_schema_root.query_type, name='Entitlements', variables=dict(query=sgqlc.types.Arg(sgqlc.types.non_null(_schema.FetchEntitlementsQuery))))
    _op_entitlements = _op.cached_entitlements(query=sgqlc.types.Variable('query'), __alias__='entitlements')
    _op_entitlements.__fragment__(fragment_entitlement_fragment())
    return _op


class Query:
    entitlements = query_entitlements()
    get_coupons = query_get_coupons()
    get_customer_by_id = query_get_customer_by_id()
    get_paywall = query_get_paywall()


class Operations:
    fragment = Fragment
    mutation = Mutation
    query = Query
