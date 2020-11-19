import Tooltip from '@material-ui/core/Tooltip';
import { withStyles, makeStyles } from "@material-ui/core/styles";

const LightTooltip = withStyles((theme) => ({
  tooltip: {
    backgroundColor: "#fcf8c0",
    color: 'rgba(0, 0, 0, 0.87)',
    boxShadow: theme.shadows[1],
    fontSize: "1.2rem",
    marginTop: "20px"

  },
}))(Tooltip);

export default LightTooltip;