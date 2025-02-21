#pragma once

namespace reqdb {
namespace api {

class RESTServer {
public:
    explicit RESTServer(int port = 8080);

    bool start();
    void stop();

private:
    void registerEndpoints();
    
    int port_;
};

} // namespace api
} // namespace reqdb
