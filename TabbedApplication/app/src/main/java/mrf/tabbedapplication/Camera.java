package mrf.tabbedapplication;

import android.Manifest;
import android.content.Context;
import android.content.pm.PackageManager;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.DashPathEffect;
import android.graphics.Paint;
import android.graphics.SurfaceTexture;
import android.hardware.camera2.CameraAccessException;
import android.hardware.camera2.CameraCaptureSession;
import android.hardware.camera2.CameraCharacteristics;
import android.hardware.camera2.CameraDevice;
import android.hardware.camera2.CameraManager;
import android.hardware.camera2.CaptureRequest;
import android.hardware.camera2.params.StreamConfigurationMap;
import android.os.Build;
import android.os.Handler;
import android.os.HandlerThread;
import android.support.design.widget.TabLayout;
import android.support.v4.app.ActivityCompat;
import android.support.v4.content.ContextCompat;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentManager;
import android.support.v4.app.FragmentPagerAdapter;
import android.support.v4.view.ViewPager;
import android.os.Bundle;
import android.util.Size;
import android.util.SparseIntArray;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuItem;
import android.view.Surface;
import android.view.TextureView;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.CompoundButton;
import android.widget.Toast;
import android.widget.ToggleButton;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;
import java.util.Vector;

public class Camera extends AppCompatActivity {
    protected SectionsPagerAdapter mSectionsPagerAdapter;
    private ViewPager mViewPager;
    private List<Fragment> mFragments = new Vector<>();
    public class Box extends View {
        private Paint paint = new Paint();
        Box(Context context) {
            super(context);
        }

        @Override
        protected void onDraw(Canvas canvas) { // Override the onDraw() Method
            super.onDraw(canvas);

            paint.setStyle(Paint.Style.STROKE);
            paint.setColor(Color.parseColor("#FF4081"));
            paint.setStrokeWidth(10);
            paint.setPathEffect(new DashPathEffect(new float[] {60,20}, 30));
            //center
            int x0 = canvas.getWidth()/2;
            int y0 = canvas.getHeight()/2;
            int dx = canvas.getHeight()/4;
            int dy = canvas.getHeight()/4;
            //draw guide box
            canvas.drawRect(x0-dx, y0-65-dy, x0+dx, y0-65+dy, paint);
        }
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_camera);
//        Box guideBox = new Box(this);
//        addContentView(guideBox, new ViewGroup.LayoutParams(ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT));
        mFragments.add(new cameraFragment());
        mFragments.add(new galleryFragment());
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.CAMERA)
                == PackageManager.PERMISSION_DENIED){
            ActivityCompat.requestPermissions(this, new String[] {Manifest.permission.CAMERA}, 1);
        }
        Toolbar toolbar = findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);
        mSectionsPagerAdapter = new SectionsPagerAdapter(getSupportFragmentManager());

        mViewPager = findViewById(R.id.container);
        mViewPager.setAdapter(mSectionsPagerAdapter);

        TabLayout tabLayout = findViewById(R.id.tabs);

        mViewPager.addOnPageChangeListener(new TabLayout.TabLayoutOnPageChangeListener(tabLayout));
        tabLayout.addOnTabSelectedListener(new TabLayout.ViewPagerOnTabSelectedListener(mViewPager));
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }

    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_camera, menu);
        return true;
    }

    public static class cameraFragment extends Fragment {
        private static final String ARG_SECTION_NUMBER = "1";
        private static final int REQUEST_CAMERA_PERMISSION_RESULT = 0;

        private CaptureRequest.Builder mCaptureRequestBuilder;
        private CameraDevice mCameraDevice;
        private Button captureButton;
        private ToggleButton toggleFlashBtn;
        private View rootView;
        private TextureView mTextureView;
        private HandlerThread mBackgroundHandlerThread;
        private Handler mBackgroundHandler;
        private String mCameraId;
        private Size mPreviewSize;

        private static SparseIntArray ORIENTATIONS = new SparseIntArray();
        static {
            ORIENTATIONS.append(Surface.ROTATION_0, 0);
            ORIENTATIONS.append(Surface.ROTATION_90, 90);
            ORIENTATIONS.append(Surface.ROTATION_180, 180);
            ORIENTATIONS.append(Surface.ROTATION_270, 270);
        }

        public cameraFragment() {}

        public static cameraFragment newInstance(int sectionNumber) {
            cameraFragment fragment = new cameraFragment();
            Bundle args = new Bundle();
            args.putInt(ARG_SECTION_NUMBER, sectionNumber);
            fragment.setArguments(args);
            return fragment;
        }

        @Override
        public View onCreateView(LayoutInflater inflater, ViewGroup container,
                                 Bundle savedInstanceState) {
            rootView = inflater.inflate(R.layout.fragment_camera, container, false);

            mTextureView = rootView.findViewById(R.id.texture);

            captureButton = rootView.findViewById(R.id.btn_takepicture);
            assert captureButton != null;
            captureButton.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    return;
                }
            });

            toggleFlashBtn = rootView.findViewById(R.id.toggleFlashBtn);
            assert toggleFlashBtn != null;
            toggleFlashBtn.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
                @Override
                public void onCheckedChanged(CompoundButton compoundButton, boolean isChecked) {
                    CameraManager cameraManager = (CameraManager) getActivity().getSystemService(Context.CAMERA_SERVICE);
                    try {
                        for (String cameraId : cameraManager.getCameraIdList()) {
                            CameraCharacteristics cameraCharacteristics = cameraManager.getCameraCharacteristics(cameraId);
                            if (cameraCharacteristics.get(cameraCharacteristics.LENS_FACING) ==
                                    CameraCharacteristics.LENS_FACING_FRONT) {
                                continue;
                            }
                            //cameraManager.setTorchMode(cameraId, true);
                            if (isChecked) {
                                Toast.makeText(getActivity(), "flash is on", Toast.LENGTH_LONG).show();
//                                cameraManager.setTorchMode(cameraId, true);
                            } else {
                                Toast.makeText(getActivity(), "flash is off", Toast.LENGTH_LONG).show();
//                                cameraManager.setTorchMode(cameraId, false);
                            }
                        }
                    }catch(CameraAccessException e){
                        e.printStackTrace();
                    }
                }
            });
            return rootView;
        }

        @Override
        public void onPause() {
            closeCamera();

            stopBackgroundThread();

            super.onPause();
        }

        @Override
        public void onResume() {
            super.onResume();

            startBackgroundThread();

            if(mTextureView.isAvailable()) {
                setupCamera(mTextureView.getWidth(), mTextureView.getHeight());
                connectCamera();
            } else {
                mTextureView.setSurfaceTextureListener(mSurfaceTextureListener);
            }
        }

        private TextureView.SurfaceTextureListener mSurfaceTextureListener = new TextureView.SurfaceTextureListener() {
            @Override
            public void onSurfaceTextureAvailable(SurfaceTexture surface, int width, int height) {
                setupCamera(width, height);
                connectCamera();
            }

            @Override
            public void onSurfaceTextureSizeChanged(SurfaceTexture surface, int width, int height) {

            }

            @Override
            public boolean onSurfaceTextureDestroyed(SurfaceTexture surface) {
                return false;
            }

            @Override
            public void onSurfaceTextureUpdated(SurfaceTexture surface) {

            }
        };

        private CameraDevice.StateCallback mCameraDeviceStateCallback = new CameraDevice.StateCallback() {
            @Override
            public void onOpened(CameraDevice camera) {
                mCameraDevice = camera;
                startPreview();
            }

            @Override
            public void onDisconnected(CameraDevice camera) {
                camera.close();
                mCameraDevice = null;
            }

            @Override
            public void onError(CameraDevice camera, int error) {
                camera.close();
                mCameraDevice = null;
            }
        };

        private static class CompareSizeByArea implements Comparator<Size> {

            @Override
            public int compare(Size lhs, Size rhs){
                return Long.signum((long) lhs.getWidth() * lhs.getHeight() /
                        (long) rhs.getWidth() * rhs.getHeight());
            }
        }

        private static int sensorToDeviceRotation(CameraCharacteristics cameraCharacteristics, int deviceOrientation){
            int sensorOrientation = cameraCharacteristics.get(CameraCharacteristics.SENSOR_ORIENTATION);
            deviceOrientation = ORIENTATIONS.get(deviceOrientation);
            return(sensorOrientation + deviceOrientation + 360) % 360;
        }

        private void closeCamera() {
            if(mCameraDevice != null) {
                mCameraDevice.close();
                mCameraDevice = null;
            }
        }

        private  void setupCamera(int width, int height) {
            CameraManager cameraManager = (CameraManager) getActivity().getSystemService(Context.CAMERA_SERVICE);
            try {
                for (String cameraId : cameraManager.getCameraIdList()) {
                    CameraCharacteristics cameraCharacteristics = cameraManager.getCameraCharacteristics(cameraId);
                    if(cameraCharacteristics.get(cameraCharacteristics.LENS_FACING) ==
                            CameraCharacteristics.LENS_FACING_FRONT){
                        continue;
                    }
                    StreamConfigurationMap map = cameraCharacteristics.get(CameraCharacteristics.SCALER_STREAM_CONFIGURATION_MAP);
                    int deviceOrientation = getActivity().getWindowManager().getDefaultDisplay().getRotation();
                    int totalRotation = sensorToDeviceRotation(cameraCharacteristics, deviceOrientation);
                    boolean swapRotation = totalRotation == 90 || totalRotation == 270;
                    int rotatedWidth = width;
                    int rotatedHeight = height;
                    if (swapRotation){
                        rotatedWidth = height;
                        rotatedHeight = width;
                    }
                    mPreviewSize = chooseOptimalSize(map.getOutputSizes(SurfaceTexture.class), rotatedWidth, rotatedHeight);
                    mCameraId = cameraId;
                    return;
                }
            } catch (CameraAccessException e) {
                e.printStackTrace();
            }
        }

        private void connectCamera() {
            CameraManager cameraManager = (CameraManager) getActivity().getSystemService(Context.CAMERA_SERVICE);
            try {
                if (Build.VERSION.SDK_INT <= Build.VERSION_CODES.M) {
                    if (ContextCompat.checkSelfPermission(getActivity(), Manifest.permission.CAMERA) ==
                            PackageManager.PERMISSION_GRANTED) {
                        cameraManager.openCamera(mCameraId, mCameraDeviceStateCallback, mBackgroundHandler);
                    } else {
                        if (shouldShowRequestPermissionRationale(Manifest.permission.CAMERA)) {
                            Toast.makeText(getActivity(), "This app requires access to camera", Toast.LENGTH_LONG).show();
                        }
                        requestPermissions(new String[]{Manifest.permission.CAMERA}, REQUEST_CAMERA_PERMISSION_RESULT);
                    }
                } else {
                    cameraManager.openCamera(mCameraId, mCameraDeviceStateCallback, mBackgroundHandler);
                }
            }catch(CameraAccessException e){
                e.printStackTrace();
            }
        }

        private void startPreview() {
            SurfaceTexture surfaceTexture = mTextureView.getSurfaceTexture();
            surfaceTexture.setDefaultBufferSize(mPreviewSize.getWidth(), mPreviewSize.getHeight());
            Surface previewSurface = new Surface(surfaceTexture);

            try {
                mCaptureRequestBuilder = mCameraDevice.createCaptureRequest(CameraDevice.TEMPLATE_PREVIEW);
                mCaptureRequestBuilder.addTarget(previewSurface);

                mCameraDevice.createCaptureSession(Arrays.asList(previewSurface),
                        new CameraCaptureSession.StateCallback() {
                            @Override
                            public void onConfigured(CameraCaptureSession session) {
                                try {
                                    session.setRepeatingRequest(mCaptureRequestBuilder.build(),
                                            null, mBackgroundHandler);
                                } catch (CameraAccessException e){
                                    e.printStackTrace();
                                }
                            }

                            @Override
                            public void onConfigureFailed(CameraCaptureSession session) {
                                Toast.makeText(getActivity(), "Unable to connect to camera", Toast.LENGTH_LONG).show();
                            }
                        }, null);
            } catch (CameraAccessException e){
                e.printStackTrace();
            }
        }

        private void startBackgroundThread() {
            mBackgroundHandlerThread = new HandlerThread("mazesolver");
            mBackgroundHandlerThread.start();
            mBackgroundHandler = new Handler(mBackgroundHandlerThread.getLooper());
        }

        private void stopBackgroundThread(){
            mBackgroundHandlerThread.quitSafely();
            try {
                mBackgroundHandlerThread.join();
                mBackgroundHandlerThread = null;
                mBackgroundHandler = null;
            } catch (InterruptedException e){
                e.printStackTrace();
            }
        }

        private static Size chooseOptimalSize(Size[] choices, int width, int height) {
            List<Size> bigEnough = new ArrayList<Size>();
            for(Size option : choices){
                if(option.getHeight() == option.getWidth() * height/width &&
                        option.getWidth() >= width && option.getHeight() >= height) {
                    bigEnough.add(option);
                }
            }
            if(bigEnough.size() > 0){
                return Collections.min(bigEnough, new CompareSizeByArea());
            } else {
                return choices[0];
            }
        }
    }

    public static class galleryFragment extends Fragment {
        private static final String ARG_SECTION_NUMBER = "2";

        public galleryFragment() {}

        public static galleryFragment newInstance(int sectionNumber) {
            galleryFragment fragment = new galleryFragment();
            Bundle args = new Bundle();
            args.putInt(ARG_SECTION_NUMBER, sectionNumber);
            fragment.setArguments(args);
            return fragment;
        }

        @Override
        public View onCreateView(LayoutInflater inflater, ViewGroup container,
                                 Bundle savedInstanceState) {

            View rootView = inflater.inflate(R.layout.fragment_gallery, container, false);
            return rootView;
        }
    }


    public class SectionsPagerAdapter extends FragmentPagerAdapter {

        public SectionsPagerAdapter(FragmentManager fm) {
            super(fm);
        }

        @Override
        public Fragment getItem(int position) {
            return mFragments.get(position);
        }

        @Override
        public int getCount() {
            // Show 2 total pages.
            return 2;
        }
    }
}
