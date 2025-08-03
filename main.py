from timer_app.factories.app_factory import TimerApplicationFactory

if __name__ == '__main__':
    root, view = TimerApplicationFactory.create_application()
    root.mainloop()
