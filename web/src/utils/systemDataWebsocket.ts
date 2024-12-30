import { Session } from '/@/utils/storage';
import { getWsBaseURL } from '/@/utils/baseUrl';
import mittBus from '/@/utils/mitt';

class SystemDataWebSocket {
    private ws: WebSocket | null = null;

    public init() {
        const service_uid = Session.get('token');
        if (!service_uid) {
            console.error('未找到 service_uid，无法连接系统数据 WebSocket');
            return;
        }

        const wsUrl = `${getWsBaseURL()}ws/${service_uid}/system_data/`;
        this.ws = new WebSocket(wsUrl);

        this.ws.onopen = () => {
            console.log('系统数据 WebSocket 连接成功');
        };

        this.ws.onmessage = (event: MessageEvent) => {
            try {
                const data = JSON.parse(event.data);
                if (data.contentType === 'HOME_DATA') {
                    mittBus.emit('homeWebsocket', data);
                }
            } catch (error) {
                console.error('解析系统数据失败:', error);
            }
        };

        this.ws.onerror = (error) => {
            console.error('系统数据 WebSocket 发生错误:', error);
        };

        this.ws.onclose = () => {
            console.log('系统数据 WebSocket 连接关闭');
            this.ws = null;
        };
    }

    public close() {
        if (this.ws) {
            this.ws.close();
            this.ws = null;
        }
    }
}

export default new SystemDataWebSocket(); 