import { Route } from "react-router";

import { UserList, UserShow, UserCreate, UserEdit } from "../pages/user";
import { InstanceList, InstanceShow, InstanceCreate, InstanceEdit } from "../pages/instance";
import { CurrencyList, CurrencyShow, CurrencyCreate, CurrencyEdit } from "../pages/currency";
import { BrokerList, BrokerShow, BrokerCreate, BrokerEdit } from "../pages/broker";
import { AssetList, AssetShow, AssetCreate, AssetEdit } from "../pages/asset";
import { AccountGroupList, AccountGroupShow, AccountGroupCreate, AccountGroupEdit } from "../pages/account_group";
import { AccountList, AccountShow, AccountCreate, AccountEdit } from "../pages/account";

/** One route per Entity Page; each only imports its page from pages/. */
export const routes = [
  <Route key="user" path="/user">
    <Route index element={<UserList />} />
    <Route path="show/:id" element={<UserShow />} />
    <Route path="create" element={<UserCreate />} />
    <Route path="edit/:id" element={<UserEdit />} />
  </Route>,
  <Route key="instance" path="/instance">
    <Route index element={<InstanceList />} />
    <Route path="show/:id" element={<InstanceShow />} />
    <Route path="create" element={<InstanceCreate />} />
    <Route path="edit/:id" element={<InstanceEdit />} />
  </Route>,
  <Route key="currency" path="/currency">
    <Route index element={<CurrencyList />} />
    <Route path="show/:id" element={<CurrencyShow />} />
    <Route path="create" element={<CurrencyCreate />} />
    <Route path="edit/:id" element={<CurrencyEdit />} />
  </Route>,
  <Route key="broker" path="/broker">
    <Route index element={<BrokerList />} />
    <Route path="show/:id" element={<BrokerShow />} />
    <Route path="create" element={<BrokerCreate />} />
    <Route path="edit/:id" element={<BrokerEdit />} />
  </Route>,
  <Route key="asset" path="/asset">
    <Route index element={<AssetList />} />
    <Route path="show/:id" element={<AssetShow />} />
    <Route path="create" element={<AssetCreate />} />
    <Route path="edit/:id" element={<AssetEdit />} />
  </Route>,
  <Route key="account_group" path="/account_group">
    <Route index element={<AccountGroupList />} />
    <Route path="show/:id" element={<AccountGroupShow />} />
    <Route path="create" element={<AccountGroupCreate />} />
    <Route path="edit/:id" element={<AccountGroupEdit />} />
  </Route>,
  <Route key="account" path="/account">
    <Route index element={<AccountList />} />
    <Route path="show/:id" element={<AccountShow />} />
    <Route path="create" element={<AccountCreate />} />
    <Route path="edit/:id" element={<AccountEdit />} />
  </Route>,
];
