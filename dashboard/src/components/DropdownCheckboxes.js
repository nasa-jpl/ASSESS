import React from 'react';
import chroma from 'chroma-js';

import { colourOptions } from './../docs/data';
import Select from 'react-select';

const colourStyles = {
  control: styles => ({ ...styles, backgroundColor: 'white', width: "80%", marginLeft: "10%", marginRight:"10%"}),
  option: (styles, { data, isDisabled, isFocused, isSelected }) => {
    const color = chroma(data.color);
    return {
      ...styles,
      backgroundColor: isDisabled
        ? null
        : isSelected
        ? data.color
        : isFocused
        ? color.alpha(0.1).css()
        : null,
      color: isDisabled
        ? '#ccc'
        : isSelected
        ? chroma.contrast(color, 'white') > 2
          ? 'white'
          : 'black'
        : data.color,
      cursor: isDisabled ? 'not-allowed' : 'default',

      ':active': {
        ...styles[':active'],
        backgroundColor: !isDisabled && (isSelected ? data.color : color.alpha(0.3).css()),
      },
    };
  },
  multiValue: (styles, { data }) => {
    const color = chroma(data.color);
    return {
      ...styles,
      backgroundColor: color.alpha(0.1).css(),
    };
  },
  multiValueLabel: (styles, { data }) => ({
    ...styles,
    color: data.color,
  }),
  multiValueRemove: (styles, { data }) => ({
    ...styles,
    color: data.color,
    ':hover': {
      backgroundColor: data.color,
      color: 'white',
    },
  }),
};

const DropdownCheckboxes = (props) => {
    
    const options = []
    props.values.forEach(d=> {
        options.push({value: d, label: d, color: "#53647a", isDisabled: false})
    })

    const handleChange = (e) => {
        props.handleFilter(e.map(d=>d.value), props.dropdownType)
    }

    return (
        <div className="dropdown-menu-box">
            <Select
                closeMenuOnSelect={false}
                defaultValue={options}
                onChange={(e) => handleChange(e)}
                isMulti
                options={options}
                styles={colourStyles}
            />
        </div>
        
    )
}

export default DropdownCheckboxes;