import React from 'react';
import { createUseStyles } from 'react-jss';

const useStyles = createUseStyles({
    bboxSelector: {
        border: (props) => `${props.borderWidth || 2}px dotted rgb(127,255,127)`,
        borderWidth: (props) => `${props.borderWidth || 2}px`,
        position: 'absolute',
    },
});

const BBoxSelector = ({ rectangle, borderWidth = 2 }) => {
    const classes = useStyles({ borderWidth });
    return (
        <div
            className={classes.bboxSelector}
            style={{
                left: `${rectangle.left - borderWidth}px`,
                top: `${rectangle.top - borderWidth}px`,
                width: `${rectangle.width}px`,
                height: `${rectangle.height}px`,
            }}
        ></div>
    );
};
export default BBoxSelector;
