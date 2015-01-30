from nose import tools as nosetools

import ckan.plugins.toolkit as toolkit
import ckan.new_tests.factories as factories
import ckan.new_tests.helpers as helpers


class TestShowcasePackageList(helpers.FunctionalTestBase):

    '''Tests for ckanext_showcase_package_list'''

    def test_showcase_package_list_no_packages(self):
        '''
        Calling ckanext_showcase_package_list with a showcase that has no
        packages returns an empty list.
        '''
        showcase_id = factories.Dataset(type='showcase')['id']

        pkg_list = helpers.call_action('ckanext_showcase_package_list',
                                       showcase_id=showcase_id)

        nosetools.assert_equal(pkg_list, [])

    def test_showcase_package_list_works_with_name(self):
        '''
        Calling ckanext_showcase_package_list with a showcase name doesn't
        raise a ValidationError.
        '''
        showcase_name = factories.Dataset(type='showcase')['name']

        pkg_list = helpers.call_action('ckanext_showcase_package_list',
                                       showcase_id=showcase_name)

        nosetools.assert_equal(pkg_list, [])

    def test_showcase_package_list_wrong_showcase_id(self):
        '''
        Calling ckanext_showcase_package_list with a bad showcase id raises a
        ValidationError.
        '''
        factories.Dataset(type='showcase')['id']

        nosetools.assert_raises(toolkit.ValidationError, helpers.call_action,
                                'ckanext_showcase_package_list',
                                showcase_id='a-bad-id')

    def test_showcase_package_list_showcase_has_package(self):
        '''
        Calling ckanext_showcase_package_list with a showcase that has a
        package should return that package.
        '''
        sysadmin = factories.User(sysadmin=True)

        package = factories.Dataset()
        showcase_id = factories.Dataset(type='showcase')['id']
        context = {'user': sysadmin['name']}
        # create an association
        helpers.call_action('ckanext_showcase_package_association_create',
                            context=context, package_id=package['id'],
                            showcase_id=showcase_id)

        pkg_list = helpers.call_action('ckanext_showcase_package_list',
                                       showcase_id=showcase_id)

        # We've got an item in the pkg_list
        nosetools.assert_equal(len(pkg_list), 1)
        # The list item should have the correct name property
        nosetools.assert_equal(pkg_list[0]['name'], package['name'])

    def test_showcase_package_list_showcase_has_two_packages(self):
        '''
        Calling ckanext_showcase_package_list with a showcase that has two
        packages should return the packages.
        '''
        sysadmin = factories.User(sysadmin=True)

        package_one = factories.Dataset()
        package_two = factories.Dataset()
        showcase_id = factories.Dataset(type='showcase')['id']
        context = {'user': sysadmin['name']}
        # create first association
        helpers.call_action('ckanext_showcase_package_association_create',
                            context=context, package_id=package_one['id'],
                            showcase_id=showcase_id)
        # create second association
        helpers.call_action('ckanext_showcase_package_association_create',
                            context=context, package_id=package_two['id'],
                            showcase_id=showcase_id)

        pkg_list = helpers.call_action('ckanext_showcase_package_list',
                                       showcase_id=showcase_id)

        # We've got two items in the pkg_list
        nosetools.assert_equal(len(pkg_list), 2)

    def test_showcase_package_list_package_isnot_a_showcase(self):
        '''
        Calling ckanext_showcase_package_list with a package id should raise a
        ValidationError.

        Since Showcases are Packages under the hood, make sure we treat them
        differently.
        '''
        sysadmin = factories.User(sysadmin=True)

        package = factories.Dataset()
        showcase_id = factories.Dataset(type='showcase')['id']
        context = {'user': sysadmin['name']}
        # create an association
        helpers.call_action('ckanext_showcase_package_association_create',
                            context=context, package_id=package['id'],
                            showcase_id=showcase_id)

        nosetools.assert_raises(toolkit.ValidationError, helpers.call_action,
                                'ckanext_showcase_package_list',
                                showcase_id=package['id'])


class TestPackageShowcaseList(helpers.FunctionalTestBase):

    '''Tests for ckanext_package_showcase_list'''

    def test_package_showcase_list_no_showcases(self):
        '''
        Calling ckanext_package_showcase_list with a package that has no
        showcases returns an empty list.
        '''
        package_id = factories.Dataset()['id']

        showcase_list = helpers.call_action('ckanext_package_showcase_list',
                                            package_id=package_id)

        nosetools.assert_equal(showcase_list, [])

    def test_package_showcase_list_works_with_name(self):
        '''
        Calling ckanext_package_showcase_list with a package name doesn't
        raise a ValidationError.
        '''
        package_name = factories.Dataset()['name']

        showcase_list = helpers.call_action('ckanext_package_showcase_list',
                                            package_id=package_name)

        nosetools.assert_equal(showcase_list, [])

    def test_package_showcase_list_wrong_showcase_id(self):
        '''
        Calling ckanext_package_showcase_list with a bad package id raises a
        ValidationError.
        '''
        factories.Dataset()['id']

        nosetools.assert_raises(toolkit.ValidationError, helpers.call_action,
                                'ckanext_package_showcase_list',
                                showcase_id='a-bad-id')

    def test_package_showcase_list_showcase_has_package(self):
        '''
        Calling ckanext_package_showcase_list with a package that has a
        showcase should return that showcase.
        '''
        sysadmin = factories.User(sysadmin=True)

        package = factories.Dataset()
        showcase = factories.Dataset(type='showcase')
        context = {'user': sysadmin['name']}
        # create an association
        helpers.call_action('ckanext_showcase_package_association_create',
                            context=context, package_id=package['id'],
                            showcase_id=showcase['id'])

        showcase_list = helpers.call_action('ckanext_package_showcase_list',
                                            package_id=package['id'])

        # We've got an item in the showcase_list
        nosetools.assert_equal(len(showcase_list), 1)
        # The list item should have the correct name property
        nosetools.assert_equal(showcase_list[0]['name'], showcase['name'])

    def test_package_showcase_list_showcase_has_two_packages(self):
        '''
        Calling ckanext_package_showcase_list with a package that has two
        showcases should return the showcases.
        '''
        sysadmin = factories.User(sysadmin=True)

        package = factories.Dataset()
        showcase_one = factories.Dataset(type='showcase')
        showcase_two = factories.Dataset(type='showcase')
        context = {'user': sysadmin['name']}
        # create first association
        helpers.call_action('ckanext_showcase_package_association_create',
                            context=context, package_id=package['id'],
                            showcase_id=showcase_one['id'])
        # create second association
        helpers.call_action('ckanext_showcase_package_association_create',
                            context=context, package_id=package['id'],
                            showcase_id=showcase_two['id'])

        showcase_list = helpers.call_action('ckanext_package_showcase_list',
                                            package_id=package['id'])

        # We've got two items in the showcase_list
        nosetools.assert_equal(len(showcase_list), 2)

    def test_package_showcase_list_package_isnot_a_showcase(self):
        '''
        Calling ckanext_package_showcase_list with a showcase id should raise a
        ValidationError.

        Since Showcases are Packages under the hood, make sure we treat them
        differently.
        '''
        sysadmin = factories.User(sysadmin=True)

        package = factories.Dataset()
        showcase = factories.Dataset(type='showcase')
        context = {'user': sysadmin['name']}
        # create an association
        helpers.call_action('ckanext_showcase_package_association_create',
                            context=context, package_id=package['id'],
                            showcase_id=showcase['id'])

        nosetools.assert_raises(toolkit.ValidationError, helpers.call_action,
                                'ckanext_package_showcase_list',
                                package_id=showcase['id'])