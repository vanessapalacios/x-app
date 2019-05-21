import React from 'react';
import { shallow } from 'enzyme';

import UsersList from '../UsersList';
import renderer from 'react-test-renderer';

const users = [
    {
        'active': true,
        'email': 'fiorellapalacios@gmail.com',
        'id': 1,
        'username': 'fiorella'
    },
    {
        'activa': true,
        'email': 'fiorellapalacios@upeu.edu.pe',
        'id': 2,
        'username': 'vanessa'
    }
];
test('UsersList renders properly', () => {
    const tree = renderer.create(<UsersList users={users}/>).toJSON();
    expect(tree).toMatchSnapshot();
});