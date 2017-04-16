# new site structure
SITE_STRUCTURE = [
    dict(
        type='LIMS Setup',
        id='lims_setup',
        title=u'LIMS Setup',
        excludeFromNav=True,
        _children = [
            dict(
                type='Lab',
                id='laboratory',
                title=u'Laboratory Information',
                excludeFromNav=True
            ),
            dict(
                type='Instruments',
                id='instruments',
                title=u'Instruments',
                excludeFromNav=True
            ),
            dict(
                type='Suppliers',
                id='supplierss',
                title=u'Suppliers',
                excludeFromNav=True
            )
        ]
    ),
    dict(
        type='Methods',
        id='methods',
        title=u'Methods'
    )
]
