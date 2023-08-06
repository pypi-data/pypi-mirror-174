# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['smcdk',
 'smcdk.api',
 'smcdk.deps.h264_profile_level_id',
 'smcdk.deps.sdp_transform',
 'smcdk.handlers',
 'smcdk.handlers.sdp',
 'smcdk.log',
 'smcdk.models']

package_data = \
{'': ['*'], 'smcdk': ['deps/*']}

install_requires = \
['aiortc>=1.2.0,<2.0.0', 'pydantic>=1.8.1,<2.0.0', 'pyee>=8.1.0,<9.0.0']

setup_kwargs = {
    'name': 'smcdk',
    'version': '1.0.0',
    'description': "mediasoup-client-pysdk, a simple mediasoup client development kit, i.e. 'smcdk', fork from pymediasoup and do more",
    'long_description': '# Mediasoup-Client-PySDK (aka "smcdk")\na simple-to-use, pure python sdk of [mediasoup](https://mediasoup.org/) client, fork from [pymediasoup](https://github.com/skymaze/pymediasoup) and do more.\n\n## Usage\nFor the purpose of to be an easy-to-use SDK, smcdk API design focus mainly on high level, and for users who know little about the official mediasoup client API. \n\n```python\nfrom smcdk import *\n\nmediasoup_client = MediasoupClient(...)\nmediasoup_client.joinRoom(...)\nmediasoup_client.play(...)\nmediasoup_client.close()\n```\nmore details, please see: examples/sdkApiDemo.py\n\n## Why another mediasoup-client?( My Personal Option, for reference only)\nThere are several official and unofficial client implementations, but they are not quick and easy to run on all OS\'s desktop, so are not suitable to be a general SDK: \n1. official client with official dependency lib\n- mediasoup-demo/aiortc: because it is based on Unix Socket, so it can\'t run in Windows\n- mediasoup-demo/broadcasters: it is based on bash language, which is good at integrating command line tools, but is not good at developing new features\n- mediasoup-demo/app: it can only run in browsers, and Electron-like desktop environment with less disk space occupation, or run in Node.js with more space occupation because of the node_modules directory\n- mediasoup-broadcast-demo: it\'s quite hard to compile and link a libwebrtc dependency successfully on all OS platform, especially in China mainland\'s network environment\n\n2. no-official client\n- pymediasoup： it is quite nice, but its API is a little hard to quick start as SDK\n\n## Architecture & Design\n![image](resources/architecture.png)\n\n### Mediasoup Client\nit contains:\n- Mediasoup Signaler Interface: follow the semantics of mediasoup-demo/server\n- Loop Tasks & Listeners: to tackle signaler request and notification from server side\n- Room and Peer: a group of simple APIs to be integrated to Listeners\n- Multimedia Runtime: a stateful mediasoup Device\n\n### Business Domain Based Listener Design\nThere are several business domain in SDK design:\nBandwidth, Peer, Producer, Consumer, DataConsumer, result in 2 request listeners\nand 5 notification listeners, which their Respective interesting events to listen and tackle\n1. Server Request\n- Consumer Listener event: newConsumer\n- DataConsumer Listener event: newDataConsumer\n2. Server Notification\n- Bandwidth Listener event: downlinkBwe\n- Peer Listener event: newPeer, peerClosed, peerDisplayNameChanged, activeSpeaker\n- Producer Listener event: producerScore\n- Consumer Listener event: consumerLayersChanged, consumerScore, consumerClosed, consumerPaused, consumerResumed\n- DataConsumer Listener event: dataConsumerClosed\n\n## Features\nTo be an easy-to-use sdk for mediasoup client development\n- **quick to run**: as mentioned above\n- **all os platform friendly**: as mentioned above\n- **signaling pluggable**: based on the mediasoup\'s design goal of "signaling agnostic", \n    >Be signaling agnostic: do not mandate any signaling protocol.”\n   \n    (sited from [mediasoup :: Overview](https://mediasoup.org/documentation/overview/)). \n    smcdk provide an out-of-box ProtooSignaler furthermore. \n    Besides the default built-in signaler, which is used to communicate with mediasoup-demo/server, \n    you can provide your own MediasoupSignalerInterface implementation to meet your requirement.\n- **listener customizable**: currently, you can customize 2 request listeners and 5 notification listeners \n## About Code Style\n  You can see many Camel-Case-Style naming in my Python code, \ne.g. "getRouterRtpCapabilities", not "get_router_rtp_capabilities".\n  The reason is not only that I began my career as a Java developer since 2008,\nbut also that I hope this SDK can be applied by those developers who use Python as a no-major language, \nand developers who have learned mediasoup by its demo app & server.\n  Maybe sometime in the future, I\'ll change this naming to follow Python’s PEP8 rules.\n## LICENSE\nMIT\n\n## Thanks\nspecial thanks to pymediasoup, mediasoup, and aiortc projects\n',
    'author': 'Jim DG',
    'author_email': 'jimdragongod@126.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/jimdragongod/mediasoup-client-pysdk',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.0,<4.0.0',
}


setup(**setup_kwargs)
