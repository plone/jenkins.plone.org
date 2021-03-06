#!/bin/sh
pip install -r requirements.txt
buildout buildout:git-clone-depth=1 -c py3.cfg
cat bin/test

return_code="all_right"

# using the alltests recipe runs not enough tests (need to investigate)...
# bin/alltests -vvv --xml || return_code=$?

# running all tests breaks test-isolation. See https://github.com/plone/Products.CMFPlone/issues/2459 ...
# ./bin/test --xml -vvv

# run many tests...
./bin/test --all --xml -vvv -s borg.localrole -s collective.monkeypatcher -s diazo -s five.customerize -s five.intid -s five.localsitemanager -s icalendar -s plone.alterego -s plone.api -s plone.app.caching -s plone.app.content -s plone.app.contentlisting -s plone.app.contentmenu -s plone.app.contentrules -s plone.app.contenttypes -s plone.app.customerize -s plone.app.dexterity -s plone.app.discussion -s plone.app.event -s plone.app.i18n -s plone.app.intid -s plone.app.iterate -s plone.app.layout -s plone.app.linkintegrity -s plone.app.locales -s plone.app.lockingbehavior -s plone.app.multilingual -s plone.app.portlets -s plone.app.querystring -s plone.app.redirector -s plone.app.registry -s plone.app.relationfield -s plone.app.testing -s plone.app.textfield -s plone.app.theming -s plone.app.upgrade -s plone.app.users -s plone.app.uuid -s plone.app.viewletmanager -s plone.app.vocabularies -s plone.app.widgets -s plone.app.workflow -s plone.app.z3cform -s plone.autoform -s plone.batching -s plone.behavior -s plone.browserlayer -s plone.cachepurging -s plone.caching -s plone.contentrules -s plone.dexterity -s plone.event -s plone.formwidget.namedfile -s plone.formwidget.recurrence -s plone.i18n -s plone.indexer -s plone.intelligenttext -s plone.keyring -s plone.locking -s plone.memoize -s plone.namedfile -s plone.outputfilters -s plone.portlet.collection -s plone.portlet.static -s plone.portlets -s plone.protect -s plone.recipe.zope2instance -s plone.registry -s plone.resource -s plone.resourceeditor -s plone.rfc822 -s plone.scale -s plone.schema -s plone.schemaeditor -s plone.session -s plone.stringinterp -s plone.subrequest -s plone.supermodel -s plone.synchronize -s plone.testing -s plone.theme -s plone.transformchain -s plone.transformchain -s plone.uuid -s plone.z3cform -s plonetheme.barceloneta -s Products.CMFCore -s Products.CMFDiffTool -s Products.CMFDynamicViewFTI -s Products.CMFPlacefulWorkflow -s Products.CMFPlone -s Products.CMFQuickInstallerTool -s Products.CMFUid -s Products.DateRecurringIndex -s Products.DCWorkflow -s Products.ExtendedPathIndex -s Products.GenericSetup -s Products.MimetypesRegistry -s Products.PlonePAS -s Products.PluggableAuthService -s Products.PluginRegistry -s Products.PortalTransforms -s Products.ResourceRegistries -s Products.statusmessages -s Products.ZCatalog -s Products.ZopeVersionControl -s repoze.xmliter -s z3c.form -s z3c.formwidget.query -s z3c.relationfield -s zope.globalrequest -s plone.app.versioningbehavior -s Products.CMFFormController -s Products.CMFEditions -s plone.folder

if [ $return_code = "all_right" ]; then
    return_code=$?
fi

# Keep tests return code
exit $return_code
