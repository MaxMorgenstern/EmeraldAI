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
    // private int mWidth, mHeight
    private float mScale, mTranslateWidth, mTranslateHeight;
    private int mDuration;
    private long mStart;
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
            setGifImageResource(id);
        }
    }


    private void init() {
        setFocusable(true);
        mMovie = Movie.decodeStream(mInputStream);
        //mWidth = mMovie.width();
        //mHeight = mMovie.height();
        mDuration = mMovie.duration();
        if (mDuration == 0) {
            mDuration = 1000;
        }

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

        //int relTime = (int) ((now - mStart) % mDuration);

        // Blink all 10 seconds
        int relTime = (int) ((now - mStart));
        if(relTime > 10000) {
            mStart = now;
        }

        Log.i(TAG, "current time: " + relTime);

        mMovie.setTime(relTime);

        canvas.scale(mScale, mScale);
        canvas.translate(mTranslateWidth, mTranslateHeight);

        mMovie.draw(canvas, 0, 0);
        invalidate();
    }

    public void setGifImageResource(int id) {
        mInputStream = mContext.getResources().openRawResource(id);
        init();
    }

    public void setGifImageStream(InputStream stream) {
        mInputStream = stream;
        init();
    }

    public void setGifImageUri(Uri uri) {
        try {
            mInputStream = mContext.getContentResolver().openInputStream(uri);
            init();
        } catch (FileNotFoundException e) {
            Log.e("GIfImageView", "File not found");
        }
    }
}
