/*
 * Opioid2D - director
 * Copyright (c) 2006 Sami Hangaslammi <shang@iki.fi>
 * 
 * Director is the heart of the Opioid2D system. It manages scene transitions,
 * screen rendering and governs the main loop.
 * 
 * Note that lot of the director functionality that was implemented in C++ in
 * earlier alphas has been moved to Python side for easier maintenance.
 * 
 */
 
#ifndef DIRECTOR_HPP
#define DIRECTOR_HPP

#include "util.hpp"

#include <map>

#include "rendering.hpp"
#include "singleton.hpp"
#include "ticker.hpp"

#ifndef NULL
#define NULL 0
#endif

namespace opi2d
{
    class Scene;
   
    class Director : public Singleton<Director>
    {
        public:
        
        ~Director();
        
        /* The actual mainloop is implemented in Python. The only responsibility left
         * for the C++ Iterate method is to update the internal Ticker that is used by
         * other C++ subsystems.
         */
        void Iterate(int now);
        
        // Render the current scene to the display backend
        void RenderFrame();
        
        // Initialize the Ticker and frame counter
        void Start(int now);
                
        // Scene Management
        void SetScene(Scene* scene);
        inline Scene* GetScene() { return this->scene; }
        
        inline const Ticker& GetTicker() const { return this->ticker; }
        
        // The TickID is essentially a frame counter. It increases by one every frame regardless
        // of frame rate.
        inline long GetTickID() const { return tickid; }
        
        protected:
        friend class Singleton<Director>;
        Director();
        
        bool quit;
        Scene* scene;
        Ticker ticker;
        int tickid;
    };
}


#endif

