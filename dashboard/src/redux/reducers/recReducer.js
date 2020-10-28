import { FETCH_REC_LOADING, FETCH_REC_SUCCESS, FETCH_REC_ERROR } from "../actionTypes";

export default function recReducer(state = {}, action){
    switch( action.type) {
        case FETCH_REC_LOADING:
            return { ...state, loading: true };
        case FETCH_REC_SUCCESS:
            return { ...state, loading: false, rec: action.payload };
        case FETCH_REC_ERROR:
            return { ...state, loading: false, error: action.payload };
        default:
            return state
    }
}