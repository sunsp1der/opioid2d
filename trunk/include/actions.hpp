/*
 * Opioid2D - actions
 * Copyright (c) 2006 Sami Hangaslammi <shang@iki.fi>
 * 
 * This module defines the action system for controlling Nodes.
 *  
 */
#ifndef OPIACTIONS
#define OPIACTIONS

#include "util.hpp"

#include <set>
#include <vector>

#include "identified.hpp"
#include "num.hpp"
#include "vec.hpp"
#include "color.hpp"
#include "curve.hpp"

#ifndef NULL
#define NULL 0
#endif

#define STOPMODE 0
#define REPEATMODE 1
#define PINGPONGMODE 2

namespace opi2d
{
    class Action;
    typedef std::set<Action*> ActionSet;	
	
    class Node;

	/*
	 * The ActionManager is the container for currently active Actions.
	 * It is resposible for iterating through Actions each frame, activating
	 * them and pruning completed actions from memory.
	 * 
	 * The ActionManager is an internal class in the C++ implementation. It is not
	 * published to the Python API at all.
	 */
    class ActionManager
    {
        public:
        	// deletes all Actions under this ActionManager
            ~ActionManager();
			
            void AddAction(Action* action);
            void RemoveAction(Action* action);
        
            void Iterate();

        protected:
            ActionSet actions;
            
            /* Intermediate containers that are used to ensure that the actions attribute doesn't
             * get altered when we are iterating through it.
             */ 
            ActionSet to_be_deleted;
            ActionSet new_actions;
    };

	/*
	 * A callback class that is used with the SWIG Director functionality to call
	 * Python functions when certain events occur.
	 * 
	 */  
    class ActionCallbacks
    {
        public:
            ActionCallbacks() {}
            virtual ~ActionCallbacks() {}
            
            // Notify the Python side that the action has ended.
            virtual void End() = 0;
            
            // "Wake" the Python code for reasons specific to certain
            // action implementations.
            virtual void Wake() = 0;
    };

    /*
     * Base class for all actions. The Action class defines the interface for
     * all actions and implements common functionality such as time limits.
     * 
     * This class is not directly used or instantiated by Python code. The methods
     * are called from Python via specific action subclasses.
     * 
     * Extends the Identified class so that memory management of these instances is
     * handled by Python.
     * 
     * Note that some actions are only valid for Sprite objects and will crash if
     * given plain Node objects. These validity checks are done in the Python API. 
     */
    class Action : public Identified
    {
        public:
        Action();
        virtual ~Action();
    
    	// utility method for setting up a new action
        void Setup(Node* target, ActionCallbacks* callbacks);
        
        // time limit is used to automatically end an action after a certain time
        virtual void SetTimeLimit(double secs);
        
        virtual void Start() {}
        
        /* The Tick functions are called at every frame update by the ActionManager.
         * CommonTick contains the functionality common to all actions and the Tick
         * method can be overriden in sublcasses.
         */
        void CommonTick(double delta);
        virtual void Tick(double delta) {}
            
        // removes this action from the ActionManager and notifies the Python side
        void End();
       
        protected:       
        friend class ActionManager;

        Node* target;
        ActionCallbacks* callbacks;
        double time_elapsed;
        double time_limit;
    };
    
    /*
     * SmoothInterval is an utility class for adding smooth acceleration and
     * deceleration to an otherwise linear interval (such as movement).
     * 
     * The mathematical idea is that given a linear action over time, we
     * create a function that fulfills the following criteria:
     * 
     * f'(t) = 0..c when t = (0..tr)
     * f'(t) = c    when t = (tr..ts)
     * f'(t) = c..0 when t = (ts..1)
     * f(0) = 0
     * f(1) = 1
     * 
     * When we use this function to manipulate the time parameter given to
     * the linear action, we achieve a smooth ramp-up curve. 
     */ 
    class SmoothInterval
    {
    	public:
    	SmoothInterval();
    	
    	void init(floatval tr, floatval ts);
    	
    	floatval calc(floatval t);
    	
    	protected:
    	floatval tr,ts;
    	
    	// cached intermediate values for making the calculation faster
    	floatval c, c2tr, c2d, cd, trc2;    	
    };
    
    /*
     * An IntervalAction is a linear action that has a discreet start and end
     * point, such as movement from specific point A to a specific point B.
     * The important property of interval actions is that we can always calculate
     * its accurate state given time (t) between 0..1 where 0 is the beginning of
     * the action and 1 is the end.
     * 
     * For example in the case of movement, t=0 means the Node is in the starting point
     * and t=1 means it has reached the destination point and every point in between
     * can be calculated from a simple equation.
     * 
     * These properties make it possible to trivially repeat interval actions and to e.g.
     * play them backwards. Thus every interval action takes a repeatMode parameter which
     * can be either "stop", "repeat" or "pingpong".
     */ 
    class IntervalAction : public Action
    {
        public:
        IntervalAction();
        
        // utility functions for setting up the action from
        // the Python side.
        void SetInterval(double secs, int repeatMode);
        void SetSmoothing(floatval fadein, floatval fadeout);
        
        inline double GetIntervalTime();
        void Tick(double delta);
        virtual void IntervalTick(double itime) {}
                
        double interval_time;
        int repeat_mode;
        bool smooth;
        SmoothInterval smoother;
    };
    
    /*
     * Action for constantly moving a Node at a specific velocity.
     * This Action has been mostly obsoleted by the more generic
     * physics system.
     */  
    class Move : public Action
    {
        public:
        Move(const Vec2& velocity);
        virtual void Tick(double delta);
        
        void SetVelocity(const Vec2& velocity);
        void AddVelocity(const Vec2& delta);
        void MulVelocity(floatval multiplier);
        
        protected:
        Vec2 velocity;
    };
    
    /*
     * Interval action for moving a Node over a specific distance.
     */
    class MoveDelta : public IntervalAction
    {
        public:
        MoveDelta(const Vec2& delta);
        virtual void Start();
        void IntervalTick(double itime);
        
        protected:
        Vec2 start_pos;
        Vec2 delta;
    };
    
    /*
     * Interval action for moving a Node to a specific point
     */
    class MoveTo : public MoveDelta
    {
        public:
        virtual void Start();
        MoveTo(const Vec2& pos);        
    };
    
    /*
     * Interval action for smoothly changing the alpha value of a Sprite.
     */
    class AlphaFade : public IntervalAction
    {
        public:
        AlphaFade(float dstAlpha);
        void Start();
        void IntervalTick(double itime);
        
        protected:
        float start_alpha;
        float end_alpha;
        float delta_alpha;
    };
    
    /*
     * Interval action for smoothing changing the color values of a Sprite.
     */
    class ColorFade : public IntervalAction
    {
        public:
        ColorFade(const Color& color);
        void Start();
        void IntervalTick(double itime);
        
        protected:
        Color start_color;
        Color end_color;
        Color delta_color;
    };
    
    /*
     * This action does nothing but ends automatically after the given time.
     * Its only purpose is to be used in action chaining in order to delay
     * another action.
     */
    class Delay : public Action
    {
        public:
        Delay(double secs);
        
        virtual void Tick(double delta);
        
        protected:
        double time_left;
    };
    
    /*
     * Interval action for rotating a Node over a given angle (degrees)
     */
    class RotateDelta : public IntervalAction
    {
        public:
        RotateDelta(floatval delta);
        void Start();
        void IntervalTick(double itime);
        
        protected:
        floatval start_pos;
        floatval delta;
    };
    
    /*
     * Action for constantly rotating a Node at given angular speed (degrees per second).
     * This action has been made obsolete by the more generic physics system.
     */
    class Rotate : public Action
    {
        public:
        Rotate(floatval speed);
        void Tick(double delta);
        
        protected:
        floatval speed;
    };
    
    /*
     * Action for constantly shrinking or enlarging a node.
     * If the multiply parameter is true, then the scale attribute
     * of the node is multiplied by the given speed every second. If
     * it's false, then the speed value is added to the node's scale
     * every second.
     */
    class Scale : public Action
    {
        public:
        Scale(floatval speed, bool multiply=true);
        void Tick(double delta);
        
        protected:
        floatval speed;
        bool multiply;
    };
	
	/*
	 * Interval action for smoothly changing the node's scale to a
	 * certain value.
	 */
	class ScaleTo : public IntervalAction
	{
		public:
		ScaleTo(const Vec2& dstScale);
		void Start();
		void IntervalTick(double itime);
		
		protected:
		Vec2 start_scale;
		Vec2 end_scale;
		Vec2 delta_scale;
	};
    
    /*
     * The TickFunc does nothing except calls the Wake() callback method
     * every frame in order to run some Python code at each frame update.
     * If the onlyReal flag is true, then the Wake callback is called at
     * constant time intervals independent of the frame rate. 
     */
    class TickFunc : public Action
    {
        public:
        TickFunc(bool onlyReal=false);
        void Tick(double delta);
        
        protected:
        bool only_real;
    };
    
    /*
     * Moves a Node smoothly over a series of destination points.
     * See the curve.hpp and curve.cpp files for more details on
     * the algorithm.
     */
    class FollowPath : public Action
    {
        public:
        FollowPath(int numpoints, floatval lead, bool alignnode);
        void Start();
        void Tick(double delta);
        
        void SetPoint(int i, const Vec2& pt);
        void SetSpeed(floatval speed);
        
        protected:
        Curve curve;
        bool alignnode;
        floatval speed;
    };
    
    /*
     * Helper class for animating a Sprite. The C++ implementation
     * does not alter the current image of the Sprite, it just calls
     * Wake() whenever the animation frame needs to change and the
     * actual work is done by Python code.
     */
    class Animate : public Action
    {
    	public:
    	Animate(double delay);
    	void SetDelay(double delay);
    	
    	void Tick(double delta);
    	
    	
    	protected:
    	double delay;
    	double delay_left;
    };
    
    /*
     * Action that makes a Node locked facing another node. The node's
     * rotation attribute is updated every frame so that it stays aligned
     * pointing the target node.
     */
    class KeepFacing : public Action
    {
    	public:
    	KeepFacing(Node* target, int offset=0);
    	
    	void Tick(double delta);
    	
    	protected:
    	Node* dest;
    	int offset;
    };
    
    /*
     * Action for rotating a node around another node.
     * 
     */
    class OrbitAround : public Action
    {
    	public:
    	OrbitAround(Node* center, floatval speed, bool keepAligned);
    	void Start();
    	void Tick(double delta);
    	
    	protected:
    	Node* center;
    	floatval speed;
    	bool keepAligned;
    	floatval initRotation;
    	floatval range, begin;
    	
    }; 
    
    class ParticleEmitter;
    
    /*
     * Helper action used for emitting particles from ParticleEmitters.
     * See particles.hpp for more details.
     */
    class ParticleEmitterAction : public Action
    {
    	public:
    	ParticleEmitterAction(ParticleEmitter* emitter);
    	
    	void Start();
    	void Tick(double delta);
    	void Delete();
    	
    	protected:
    	ParticleEmitter* emitter;
    	floatval emit_quota;
    	floatval duration;
    	floatval next_delay;
    	int num_emits;
    };
}

#endif


