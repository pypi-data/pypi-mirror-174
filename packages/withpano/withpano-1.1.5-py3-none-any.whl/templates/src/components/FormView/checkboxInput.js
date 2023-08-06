import FormLabel from "@material-ui/core/FormLabel";
import {Checkbox} from "@material-ui/core";

const CheckBoxInput = ({label, options, required, ...rest}) => {
    return (
        <div style={{justifyContent: "space-between"}} className="flex input">
            <FormLabel component="legend">
                <Checkbox
                    size="small"
                    className="input"
                    {...rest}
                />
                {label}
            </FormLabel>
        </div>
    );
};

export default CheckBoxInput;