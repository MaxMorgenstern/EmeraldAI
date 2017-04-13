package org.EmeraldAI.FaceApp;

import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Movie;
import android.net.Uri;
import android.os.SystemClock;
import android.util.AttributeSet;
import android.util.Log;
import android.view.View;

import java.io.FileNotFoundException;
import java.io.InputStream;

import static android.content.ContentValues.TAG;

/**
 * Created by maximilianporzelt on 10.04.17.
 * Class inspired by: http://www.mavengang.com/2016/05/02/gif-animation-android/
 */

public class GifImageView extends View {

    private InputStream mInputStream;
    private Movie mMovie;
    private float mScale, mTranslateWidth, mTranslateHeight;
    private int mDuration;
    private long mStart;
    private boolean mLoop;
    private int mDelay;
    private Context mContext;

    public GifImageView(Context context) {
        super(context);
        this.mContext = context;
    }

    public GifImageView(Context context, AttributeSet attrs) {
        this(context, attrs, 0);
    }

    public GifImageView(Context context, AttributeSet attrs, int defStyleAttr) {
        super(context, attrs, defStyleAttr);
        this.mContext = context;
        if (attrs.getAttributeName(1).equals("background")) {
            int id = Integer.parseInt(attrs.getAttributeValue(1).substring(1));
            SetGifImageResource(id);
        }
    }


    private void init(InputStream inputStream, boolean loop, int delay) {
        mInputStream = inputStream;
        mLoop = loop;
        mDelay = delay;

        setFocusable(true);
        mMovie = Movie.decodeStream(mInputStream);
        mDuration = mMovie.duration();
        if (mDuration == 0) {
            mDuration = 1000;
        }
        mStart = 0;

        requestLayout();
    }

    @Override
    protected void onMeasure(int widthMeasureSpec, int heightMeasureSpec) {
        int parentWidth = MeasureSpec.getSize(widthMeasureSpec);
        int parentHeight = MeasureSpec.getSize(heightMeasureSpec);
        this.setMeasuredDimension(parentWidth, parentHeight);
        super.onMeasure(widthMeasureSpec, heightMeasureSpec);
    }

    @Override
    protected void onDraw(Canvas canvas) {
        if (mMovie == null)
            return;

        long now = SystemClock.uptimeMillis();

        if (mStart == 0 ) {
            mStart = now;
            mScale = Math.min((float)getWidth() / mMovie.width(), (float)getHeight() / mMovie.height());
            mTranslateWidth = ((float)getWidth() / mScale - (float)mMovie.width())/2f;
            mTranslateHeight = ((float)getHeight() / mScale - (float)mMovie.height())/2f;
        }

        int relTime = 0;
        // loop with delay
        if(mLoop && mDelay > 0) {
            relTime = (int) ((now - mStart));
            if(relTime >= (mDelay+mDuration)) {
                mStart = now;
            }
        // loop without delay
        } else if(mLoop){
            relTime = (int) ((now - mStart) % mDuration);
        // play once
        } else {
            relTime = (int) ((now - mStart));
        }

        //Log.i(TAG, "current time: " + relTime);

        mMovie.setTime(relTime);

        canvas.scale(mScale, mScale);
        canvas.translate(mTranslateWidth, mTranslateHeight);

        mMovie.draw(canvas, 0, 0);
        invalidate();
    }

    public void SetGifImageResource(int id) {
        init(mContext.getResources().openRawResource(id), true, 0);
    }
    public void SetGifImageResource(int id, boolean loop) {
        init(mContext.getResources().openRawResource(id), loop, 0);
    }
    public void SetGifImageResource(int id, boolean loop, int delay) {
        init(mContext.getResources().openRawResource(id), loop, delay);
    }

    public void SetGifImageStream(InputStream stream) {
        init(stream, true, 0);
    }
    public void SetGifImageStream(InputStream stream, boolean loop) {
        init(stream, loop, 0);
    }
    public void SetGifImageStream(InputStream stream, boolean loop, int delay) {
        init(stream, loop, delay);
    }

    public void SetGifImageUri(Uri uri) {
        try {
            init(mContext.getContentResolver().openInputStream(uri), true, 0);
        } catch (FileNotFoundException e) {
            Log.e("GIfImageView", "File not found");
        }
    }
    public void SetGifImageUri(Uri uri, boolean loop) {
        try {
            init(mContext.getContentResolver().openInputStream(uri), loop, 0);
        } catch (FileNotFoundException e) {
            Log.e("GIfImageView", "File not found");
        }
    }
    public void SetGifImageUri(Uri uri, boolean loop, int delay) {
        try {
            init(mContext.getContentResolver().openInputStream(uri), loop, delay);
        } catch (FileNotFoundException e) {
            Log.e("GIfImageView", "File not found");
        }
    }
}
