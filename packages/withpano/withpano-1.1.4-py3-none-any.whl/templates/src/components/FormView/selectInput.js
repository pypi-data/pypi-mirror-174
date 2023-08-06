import TextField from "@material-ui/core/TextField";

const SelectInput = ({options, ...rest}) => {
    return (
        <TextField
            variant="outlined"
            size="small"
            className="input"
            select
            {...rest}
            SelectProps={{native: true}}
        >
            <option defaultValue="" style={{display: "none"}}></option>
            {options.map((option) => (
                <option key={option} value={option}>
                    {option}
                </option>
            ))}
        </TextField>
    );
};

export default SelectInput;