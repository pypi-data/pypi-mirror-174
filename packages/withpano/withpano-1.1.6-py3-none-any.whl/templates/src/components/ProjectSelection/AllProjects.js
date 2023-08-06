import {PureComponent} from "react";

class AllProjects extends PureComponent {
    constructor(props) {
        super(props);

    }

    render() {
        return (
            <div>
                <Stack direction="row" spacing={2}>
                    <Item>Item 1</Item>
                    <Item>Item 2</Item>
                    <Item>Item 3</Item>
                </Stack>
            </div>
        );
    }

}