import React, { useState, useRef } from 'react';
import BBoxAnnotator from './BBoxAnnotator';
import { Button, Modal, Flex, Image, Card, Layout } from 'antd';
import axios from 'axios';
import fileDownload from 'js-file-download'

const { Header, Content } = Layout;

const MainPage = ({init, onNewProject}) => {
    const [isModalOpen, setIsModalOpen] = useState(false)
    const [lastVersion, setLastVersion] = useState(init['lastVersion'])
    const [isAdjust, setIsAdjust] = useState(init['isAdjust'])
    const annotations = useRef([])
    const id = useRef(init['id'])
    const origImgName = useRef(init['origImgName'])
    console.log(id.current)
    console.log(init['id'])

    const onAdjustOrModify = () => {
      let body = {
        id: id.current,
        annotations: annotations.current
      };
      
      axios.post(`http://127.0.0.1:5000/adjust-or-modify`, body)
        .then(function (response) {
          setLastVersion(response.data['lastVersion'])
        })
    }

    const onDownload = () => {
      axios.get(`http://127.0.0.1:5000/data/${id.current}/${lastVersion}.html`, {
        responseType: 'blob',
      })
      .then((res) => {
        fileDownload(res.data, 'index.html')
      })
    }

    const onChangeStage = () => {
        setIsAdjust(false)
        let body = {
            id: id.current,
        };
        axios.post(`http://127.0.0.1:5000/change-stage`, body)
    }

    return (
        <Layout>
            <Header 
            style={{
                position: 'sticky',
                top: 0,
                zIndex: 1,
                width: '100%',
                display: 'flex',
                alignItems: 'center',
            }}
            >
            <Flex horizontal justify={'left'} gap={'large'}>
                <Button type="primary" onClick={() => {setIsModalOpen(true)}}>Annotate</Button>
                {isAdjust ? <Button type="primary" onClick={onAdjustOrModify}>Adjust</Button> : <Button type="primary" onClick={onAdjustOrModify}>Modify</Button>}
                <Button type="primary" onClick={onDownload}>Download HTML</Button>
                {isAdjust ? <Button type="primary" onClick={onChangeStage}>Modify Further</Button> : null}
                <Button type="primary" onClick={onNewProject}>New Project</Button>
            </Flex>
            </Header>
            <Content>
            <div style={{marginTop: 50}}>
                <Flex horizontal justify={'space-around'}>
                <div style={{width: '45%'}}>
                    <Card>
                    <Image
                        src={isAdjust ? `http://127.0.0.1:5000/data/${id.current}/${origImgName.current}` : `http://127.0.0.1:5000/data/${id.current}/${lastVersion > 0 ? `${lastVersion-1}.png` : origImgName.current}`}
                    />
                    </Card>
                </div>
                <div style={{width: '45%'}}>
                    <Card>
                    <Image
                        src={`http://127.0.0.1:5000/data/${id.current}/${lastVersion}.png`}
                    />
                    </Card>
                </div>
                </Flex>
            </div>
            </Content>
            <Modal title="Basic Modal" open={isModalOpen} width={1500} onCancel={()=>setIsModalOpen(false)} onOk={()=>setIsModalOpen(false)}>
            <BBoxAnnotator
                url={`http://127.0.0.1:5000/data/${id.current}/${lastVersion}.png`}
                inputMethod='text'
                onChange={(e) => annotations.current=e}
                style={{ maxWidth: 'auto' }}
            />
            </Modal>
        </Layout>
    )
}

export default MainPage