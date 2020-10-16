import { createStore, compose, applyMiddleware } from "redux";
import thunk from "redux-thunk";
import { loadState, saveState } from "./localStorage"

import rootReducer from "./reducers";
import initialState from "./initialState"

function configureStore(initialState) {
    const enhancer = compose(applyMiddleware(thunk));
    return createStore(rootReducer, initialState, enhancer);
}

const store = configureStore(initialState);

export default store;