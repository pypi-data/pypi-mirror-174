import TextField from "@material-ui/core/TextField";

const TextInput = ({...rest}) => {
    return (
        <TextField
            variant="outlined"
            size="small"
            className="input"
            {...rest}
        />
    );
};

export default TextInput;