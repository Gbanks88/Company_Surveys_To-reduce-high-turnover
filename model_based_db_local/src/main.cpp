#include <QApplication>
#include <QCommandLineParser>
#include <spdlog/spdlog.h>
#include "gui/MainWindow.hpp"

int main(int argc, char* argv[]) {
    try {
        // Initialize logging
        spdlog::set_level(spdlog::level::info);
        spdlog::info("Starting Employee Survey System");

        // Create Qt application
        QApplication app(argc, argv);
        QApplication::setApplicationName("Employee Survey System");
        QApplication::setApplicationVersion("1.0.0");

        // Parse command line arguments
        QCommandLineParser parser;
        parser.setApplicationDescription("Employee Survey System");
        parser.addHelpOption();
        parser.addVersionOption();
        parser.process(app);

        // Create and show main window
        reqdb::gui::MainWindow mainWindow;
        mainWindow.show();
        return app.exec();

    } catch (const std::exception& e) {
        spdlog::error("Fatal error: {}", e.what());
        return 1;
    }
}
