export const getRec = (state) => {
    return state.rec.rec;
}

export const getRecLoading = (state) => state.rec.loading;
export const getRecError = (state) => state.rec.error;

export const getPdf = (state) => {
    return state.pdf.pdf;
}

export const getPdfLoading = (state) => state.pdf.loading;
export const getPdfError = (state) => state.pdf.error;