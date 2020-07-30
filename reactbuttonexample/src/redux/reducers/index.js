import { combineReducers } from "redux";
import recReducer from "./recReducer";

export default combineReducers({
    rec: recReducer
})