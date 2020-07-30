import { FETCH_REC_LOADING, FETCH_REC_SUCCESS, FETCH_REC_ERROR } from "../actionTypes";
import PdfViewer from "../../components/PdfViewer";

export function fetchRecLoading() {
    return {
        type: FETCH_REC_LOADING,
    };
}

export function fetchRecSuccess(recommendation){
    return {
        type: FETCH_REC_SUCCESS,
        payload: recommendation,
    }
}

export function fetchRecError(error){
    return {
        type: FETCH_REC_ERROR,
        payload: error
    }
}