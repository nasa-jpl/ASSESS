import { FETCH_PDF_LOADING, FETCH_PDF_SUCCESS, FETCH_PDF_ERROR } from "../actionTypes";

export default function PdfReducer(state = {}, action){
    switch( action.type) {
        case FETCH_PDF_LOADING:
            return { ...state, loading: true };
        case FETCH_PDF_SUCCESS:
            return { ...state, loading: false, pdf: action.payload };
        case FETCH_PDF_ERROR:
            return { ...state, loading: false, error: action.payload };
        default:
            return state
    }
}