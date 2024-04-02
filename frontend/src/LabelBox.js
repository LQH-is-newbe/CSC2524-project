import React, { useState } from 'react';
import { createUseStyles } from 'react-jss';

const useStyles = createUseStyles({
    labelBox: {
        left: (props) => `${props.left}px`,
        top: (props) => `${props.top}px`,
        position: 'absolute',
    },
    labelInput: {},
});

const LabelBox = React.forwardRef(({ inputMethod, ...props }, forwardedRef) => {
    const classes = useStyles(props);
    const [value, setValue] = useState('');
    const changeHandler = (e) => {
        setValue(e.target.value);
        if (inputMethod === 'select') {
            props.onSubmit(e.target.value);
        }
    };
    const keyPressHandler = (e) => {
        if (e.which === 13) {
            props.onSubmit(value);
        }

        return e.which !== 13;
    };
    let { labels = ['object'] } = props;
    if (typeof labels === 'string') {
        labels = [labels];
    }
    let labelInput;
    switch (inputMethod) {
        case 'select':
            labelInput = (
                <select
                    className={classes.labelInput}
                    name="label"
                    ref={forwardedRef}
                    onChange={changeHandler}
                    onMouseDown={(e) => e.stopPropagation()}
                >
                    <option>choose an item</option>
                    {labels.map((label) => (
                        <option key={label} value={label}>
                            {label}
                        </option>
                    ))}
                </select>
            );
            break;
        case 'text':
            labelInput = (
                <input
                    className={classes.labelInput}
                    name="label"
                    type="text"
                    value={value}
                    ref={forwardedRef}
                    onKeyPress={keyPressHandler}
                    onChange={changeHandler}
                    onMouseDown={(e) => e.stopPropagation()}
                />
            );
            break;
        default:
            throw `Invalid labelInput parameter: ${inputMethod}`;
    }

    return <div className={classes.labelBox}>{labelInput}</div>;
});
LabelBox.displayName = 'LabelBox';

export default LabelBox;
