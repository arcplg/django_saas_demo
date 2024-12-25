# Phân biệt Request URL và Webhook URL

## 1. Request URL

- **Sử dụng khi** bạn muốn Slack gửi sự kiện (events) đến server của bạn.
- Thường được sử dụng trong các **Slack Event Subscriptions** hoặc các app tương tác qua **Slash Commands**, **Interactive Components**.
- Ví dụ: Slack gửi sự kiện khi có người nhắn tin trong kênh, app của bạn xử lý rồi phản hồi lại.

## 2. Webhook URL

- **Sử dụng để** app của bạn gửi thông tin ngược lại Slack, ví dụ: thông báo trong một channel.
- **Không tự động nhận sự kiện** từ Slack. Bạn chỉ gọi webhook khi bạn muốn gửi một tin nhắn hoặc action cụ thể lên Slack.
- Webhook URL là một endpoint do Slack cung cấp, bạn **không cần tự xây dựng**.

---

## Khi nào nên dùng Webhook URL thay vì Request URL?

- Nếu app của bạn chỉ gửi thông báo hoặc dữ liệu lên Slack mà không cần nhận sự kiện từ Slack.
- **Không cần sử dụng ngrok** hay expose server cục bộ.
- Slack cung cấp sẵn **webhook URL**, bạn chỉ cần gọi nó qua HTTP POST.

---

## Khi nào nên dùng Request URL?

- Khi bạn cần nhận sự kiện từ Slack (như tin nhắn, tương tác với button, hoặc slash command).
- Dùng với **Event Subscriptions**, **Slash Commands**, hoặc **Interactive Components**.

---

## Socket Mode là gì?

- **Socket Mode** là một cách khác để kết nối ứng dụng của bạn với Slack mà không cần expose server của bạn ra Internet. Thay vì Slack gửi các sự kiện qua HTTP (Request URL), nó sử dụng **WebSocket** để gửi sự kiện đến ứng dụng của bạn.
- Socket Mode rất hữu ích khi bạn không muốn sử dụng **tunneling tools** (như ngrok) hoặc khi ứng dụng của bạn hoạt động cục bộ, phía sau tường lửa, hoặc không có **public IP**.

---

## Cách hoạt động của Socket Mode

1. Ứng dụng của bạn mở một kết nối **WebSocket** với Slack.
2. Slack gửi các sự kiện (event payloads) qua kết nối WebSocket đó.
3. Ứng dụng xử lý các sự kiện và thực hiện hành động cần thiết (như phản hồi tin nhắn hoặc gửi thông báo).

---

## Ưu điểm của Socket Mode

- **Không cần Request URL**: Không cần expose máy chủ ra Internet.
- **An toàn hơn**: Không có endpoint công khai, giảm rủi ro tấn công.
- **Linh hoạt**: Hoạt động ngay cả khi ứng dụng chạy cục bộ hoặc phía sau tường lửa.

---

## Khi nào nên dùng Socket Mode?

- Bạn không muốn sử dụng **tunneling tools** như ngrok.
- Server của bạn không thể dễ dàng truy cập từ Internet (ví dụ: chạy phía sau tường lửa).
- Bạn muốn ứng dụng giao tiếp với Slack qua một kết nối ổn định, không cần gửi nhiều yêu cầu HTTP.

---

## Ưu điểm của Socket Mode khi public app

- **Không cần expose server**: Socket Mode không yêu cầu bạn phải mở cổng hoặc host server công khai trên Internet, giảm thiểu các vấn đề bảo mật liên quan đến việc expose endpoint.
- **Tương thích với Slack App Directory**: Slack hỗ trợ đầy đủ Socket Mode cho cả ứng dụng nội bộ (internal) và ứng dụng công khai (public).
- **Đơn giản hóa cấu hình**: Không cần khách hàng phải thiết lập Request URL, bạn chỉ cần giữ quản lý **App-Level Token** và duy trì kết nối WebSocket từ server của bạn.

---

## Request URL - Tại sao vẫn tồn tại?

**Request URL** (có thể gọi là HTTP endpoint) là phương pháp truyền thống mà Slack sử dụng để gửi sự kiện đến các ứng dụng của bạn. Khi một sự kiện xảy ra trong Slack (ví dụ: tin nhắn mới, tương tác với button), Slack sẽ gửi một HTTP request đến URL mà bạn cung cấp (request URL).

### Ưu điểm của Request URL:

- **Phân tán tải**: Các sự kiện từ Slack sẽ được gửi đến nhiều endpoint khác nhau của các ứng dụng. Điều này giúp phân tán tải dễ dàng hơn và tránh trường hợp tải cao tại một điểm.
- **Quy trình HTTP đơn giản**: Việc sử dụng HTTP/HTTPS rất dễ triển khai. Các hệ thống web hiện đại đều hỗ trợ các request HTTP mà không cần thêm cấu hình phức tạp.
- **Tương thích rộng rãi**: Request URL dễ dàng tích hợp với các hệ thống ngoài Slack, nơi không cần WebSocket. Nếu app của bạn tích hợp với các công nghệ khác không sử dụng WebSocket (ví dụ: các hệ thống RESTful API), việc sử dụng Request URL giúp đồng bộ hoá công việc.
- **Quy trình bảo mật đơn giản**: Với Request URL, bạn có thể dễ dàng triển khai bảo mật bằng cách yêu cầu các headers xác thực, xác nhận tính hợp lệ của các sự kiện từ Slack, cũng như mã hóa và bảo mật dữ liệu thông qua HTTPS.

---

## Socket Mode - Tại sao lại cần Socket Mode?

**Socket Mode** là cách tiếp cận hiện đại và thích hợp cho các trường hợp ứng dụng cần nhận sự kiện theo thời gian thực, hoặc khi ứng dụng không thể sử dụng các Request URL (ví dụ: khi ứng dụng chạy trên môi trường cục bộ, phía sau tường lửa).

### Ưu điểm của Socket Mode:

- **Không cần expose server ra ngoài Internet**: Socket Mode giúp bạn tránh được việc phải expose HTTP endpoints của mình ra ngoài, điều này cực kỳ hữu ích khi bạn muốn bảo vệ server của mình khỏi các cuộc tấn công từ bên ngoài.
- **Kết nối thời gian thực**: Socket Mode sử dụng WebSocket, giúp các sự kiện từ Slack đến ứng dụng của bạn gần như ngay lập tức (real-time). Điều này rất hữu ích khi bạn cần phản hồi ngay lập tức hoặc khi có nhiều sự kiện cần được xử lý ngay lập tức mà không phải chờ đợi HTTP request.
- **Quản lý kết nối đơn giản hơn trong môi trường cloud**: Nếu bạn deploy ứng dụng trên các nền tảng cloud mà không muốn mở cổng HTTP (như AWS Lambda hoặc môi trường không có IP public), Socket Mode giúp giảm bớt yêu cầu cấu hình hạ tầng.
- **Không bị giới hạn bởi các request HTTP**: Trong môi trường có nhiều sự kiện liên tục từ Slack, việc dùng WebSocket sẽ giảm tải cho hệ thống và giúp ứng dụng của bạn xử lý sự kiện hiệu quả hơn.

---

## Tại sao Slack cung cấp cả hai phương pháp?

Slack cung cấp **Request URL** và **Socket Mode** để phục vụ các nhu cầu khác nhau của ứng dụng và hạ tầng của người dùng.

### Lý do sử dụng Request URL:

- **Đơn giản và quen thuộc**: Các ứng dụng web phổ thông đã quen với mô hình HTTP request-response. Nếu bạn đang triển khai một ứng dụng web truyền thống, không có lý do gì để sử dụng Socket Mode.
- **Tính tương thích rộng**: Request URL hoạt động với hầu hết các loại ứng dụng và server, bao gồm các hệ thống không sử dụng WebSocket.

### Lý do sử dụng Socket Mode:

- **Thời gian thực và bảo mật**: Khi bạn cần có sự phản hồi ngay lập tức từ ứng dụng của mình và không muốn expose HTTP endpoints ra ngoài.
- **Không phải cấu hình server công khai**: Khi bạn muốn ứng dụng của mình hoạt động trong môi trường không có IP public hoặc không muốn quản lý nhiều endpoint HTTP.

---

## Tóm lại: Sự khác biệt giữa Request URL và Socket Mode

| **Tiêu chí**                | **Request URL**                                | **Socket Mode**                               |
|-----------------------------|------------------------------------------------|-----------------------------------------------|
| **Cơ chế giao tiếp**         | HTTP request-response (RESTful)                | WebSocket (kết nối thời gian thực, liên tục)  |
| **Cần expose server ra ngoài Internet?** | Có (cần mở cổng hoặc sử dụng tunneling tool như ngrok) | Không cần, kết nối trực tiếp qua WebSocket    |
| **Mức độ phức tạp**          | Đơn giản, dễ triển khai                        | Phức tạp hơn, yêu cầu kết nối WebSocket      |
| **Tình huống sử dụng**       | Các ứng dụng web truyền thống, tích hợp với REST API khác | Ứng dụng cần kết nối thời gian thực hoặc bảo mật |
| **Khả năng mở rộng**         | Có thể gặp khó khăn khi có nhiều sự kiện (scaling issues) | Dễ mở rộng và quản lý kết nối real-time      |
| **Quản lý kết nối**          | Mỗi sự kiện yêu cầu một HTTP request riêng biệt | Kết nối WebSocket duy trì suốt quá trình hoạt động |
| **Bảo mật**                  | Cần bảo vệ HTTP endpoint bằng HTTPS và các cơ chế xác thực | Cần bảo vệ App-Level Token và các kết nối WebSocket |
| **Phản hồi sự kiện**         | Phản hồi sự kiện qua HTTP request-response, có độ trễ nhất định | Phản hồi ngay lập tức qua WebSocket (real-time) |
| **Sự kiện hỗ trợ**           | Phù hợp với các sự kiện như tin nhắn, thông báo, button click | Phù hợp với tất cả các sự kiện thời gian thực từ Slack |
| **Tích hợp với các hệ thống khác** | Dễ dàng tích hợp với các API RESTful bên ngoài Slack | Khó tích hợp với các hệ thống không dùng WebSocket |

---

## Vậy, khi nào nên chọn phương pháp nào?

- **Socket Mode**: Nếu bạn cần thời gian thực, không muốn expose server, hoặc không thể sử dụng cổng HTTP công khai.
- **Request URL**: Nếu bạn cần đơn giản, không cần kết nối WebSocket, hoặc ứng dụng của bạn tích hợp với các hệ thống khác qua HTTP.
