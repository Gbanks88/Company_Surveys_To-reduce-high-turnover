#pragma once

#include <boost/beast/core.hpp>
#include <boost/beast/http.hpp>
#include <boost/beast/websocket.hpp>
#include <boost/asio/ip/tcp.hpp>
#include <string>
#include <memory>
#include <functional>
#include <nlohmann/json.hpp>

namespace eco {
namespace core {

class WebServer {
public:
    using MessageHandler = std::function<void(const nlohmann::json&, nlohmann::json&)>;

    WebServer(const std::string& address, unsigned short port);
    ~WebServer();

    // Start the server
    void start();
    
    // Stop the server
    void stop();

    // Register handlers for different endpoints
    void registerHandler(const std::string& endpoint, MessageHandler handler);

    // WebSocket broadcast
    void broadcast(const std::string& message);

    // Check if server is running
    bool isRunning() const;

private:
    class Impl;
    std::unique_ptr<Impl> impl_;

    void handleHttpRequest(boost::beast::http::request<boost::beast::http::string_body>& req);
    void handleWebSocket(boost::beast::websocket::stream<boost::beast::tcp_stream>& ws);
};

} // namespace core
} // namespace eco
