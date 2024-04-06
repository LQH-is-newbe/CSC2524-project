import React, { useRef, useState } from 'react';
import { Button, Upload, Flex, Input, Typography, Spin } from 'antd';
import { InboxOutlined } from '@ant-design/icons';
import axios from 'axios';

const { Dragger } = Upload;
const { TextArea } = Input;

const FrontPage = ({onFrontPageSubmit}) => {
    const [spinning, setSpinning] = useState(false);
    const origImg = useRef(null)
    const description = useRef("")
    const projectId = useRef("")

    const uploadProps = {
        name: 'file',
        beforeUpload: (file) => {
          origImg.current = file
          return false
        }
    }

    const onGenerate = () => {
        setSpinning(true)
        const formData = new FormData()
        formData.append('file', origImg.current)
        formData.append('description', description.current)
        axios.post('http://127.0.0.1:5000/new-project', formData)
            .then((res) => {onFrontPageSubmit(res.data)})
    }

    const onResume = () => {
        let body = {
            id: projectId.current
        }  
        axios.post(`http://127.0.0.1:5000/project`, body)
            .then((res) => onFrontPageSubmit(res.data))
    }

    return (
        <div style={{paddingTop: 100, width: '30%', margin: 'auto'}}>
            <Flex gap={'middle'} vertical>
            <Dragger {...uploadProps}>
                <p className="ant-upload-drag-icon">
                <InboxOutlined />
                </p>
                <p className="ant-upload-text">Click or drag file to this area to upload the sketch</p>
            </Dragger>
            <Flex align={'center'} vertical>
                <Typography.Text>Description</Typography.Text>
                <TextArea placeholder="How do you want your webpage be like?" onChange={(e)=>description.current=e.target.value}/>
            </Flex>
            <Button type="primary" onClick={onGenerate}>Generate!</Button>
            <Flex align={'center'} vertical>
                <Typography.Text>Project ID</Typography.Text>
                <Input placeholder="Enter the project ID to resume the project" onChange={(e)=>projectId.current=e.target.value}/>
            </Flex>
            <Button type="primary" onClick={onResume}>Resume</Button>
            </Flex>
            <Spin spinning={spinning} fullscreen />
        </div>
    )
}

export default FrontPage