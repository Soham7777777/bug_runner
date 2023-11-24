import sys

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'AI-TRAINING':
        import ai_training_loop
        ai_training_loop.run()
    else:
        import mainloop
        mainloop.play()