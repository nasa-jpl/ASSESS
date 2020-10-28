export const loadState = () => {
    try {
      const serializedState = localStorage.getItem("state");
      if (serializedState === null) {
        return {};
      }
      const state = JSON.parse(serializedState);
      return state.expiration && new Date() < new Date(state.expiration) ? state : {};
    } catch (err) {
      return {};
    }
  };
  
export const saveState = (state) => {
  try {
    state["expiration"] = new Date(new Date().getTime() + 60 * 60 * 1000 * 2);
    const serializedState = JSON.stringify(state);
    localStorage.setItem("state", serializedState);
  } catch (err) {}
};
  