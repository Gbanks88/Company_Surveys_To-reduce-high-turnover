#pragma once

#include <string>
#include <functional>

namespace reqdb {
namespace api {

class WebSocketConnection;

using ConnectionHandler = std::function<void(WebSocketConnection*)>;
using MessageHandler = std::function<void(WebSocketConnection*, const std::string&)>;

class WebSocketServer {
public:
    explicit WebSocketServer(int port = 8081);

    bool start();
    void stop();
    void broadcast(const std::string& message);

    void onConnect(const ConnectionHandler& handler);
    void onMessage(const MessageHandler& handler);
    void onDisconnect(const ConnectionHandler& handler);

private:
    int port_;
    ConnectionHandler connectHandler_;
    MessageHandler messageHandler_;
    ConnectionHandler disconnectHandler_;
};

} // namespace api
} // namespace reqdb
