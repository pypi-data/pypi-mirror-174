import Radio from "@material-ui/core/Radio";
import RadioGroup from "@material-ui/core/RadioGroup";
import FormControlLabel from "@material-ui/core/FormControlLabel";
import FormLabel from "@material-ui/core/FormLabel";

const RadioInput = ({label, options, required, ...rest}) => {
    return (
        <div style={{justifyContent: "space-between"}} className="flex input">
            <FormLabel component="legend">{label}</FormLabel>
            <RadioGroup {...rest} row>
                {options.map((option) => (
                    <FormControlLabel
                        value={option}
                        control={<Radio color="primary" required={required}/>}
                        label={option}
                        key={option}
                    />
                ))}
            </RadioGroup>
        </div>
    );
};

export default RadioInput;