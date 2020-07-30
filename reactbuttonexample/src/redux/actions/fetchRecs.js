import { fetchRecLoading, fetchRecSuccess, fetchRecError } from ".";
import DummyStandards from "./../../Report/DummyStandards";


function fetchRecs() {
    return (dispatch) => {
        dispatch(fetchRecLoading());

        dispatch(fetchRecSuccess(DummyStandards));
        return DummyStandards;
    }
}

export default fetchRecs;