import sys

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == 'AI-TRAINING':
            import ai_training_loop
            ai_training_loop.run()
        elif sys.argv[1] == 'AI-ENABLED':
            import mainloop
            mainloop.play(True)    
    else:
        import mainloop
        mainloop.play(False)