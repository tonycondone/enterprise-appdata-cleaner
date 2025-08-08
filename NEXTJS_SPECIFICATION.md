# Next.js Web Application - Technical Specification

## 🎯 Project Overview

Transform the enterprise AppData cleaner into a modern, responsive web application using Next.js 14+ with TypeScript, providing a professional interface for system administrators and DevOps teams.

---

## 🏗️ Technical Architecture

### **Tech Stack**
- **Framework**: Next.js 14+ (App Router)
- **Language**: TypeScript 5.0+
- **Styling**: Tailwind CSS + CSS Modules
- **State Management**: Zustand + React Query
- **UI Components**: Radix UI + Custom Components
- **Authentication**: NextAuth.js
- **Database**: PostgreSQL + Prisma
- **API**: Next.js API Routes + tRPC
- **Testing**: Jest + React Testing Library + Playwright
- **Deployment**: Vercel

### **Project Structure**
```
enterprise-appdata-cleaner-web/
├── app/
│   ├── (auth)/
│   │   ├── login/
│   │   └── register/
│   ├── (dashboard)/
│   │   ├── dashboard/
│   │   ├── cleanup/
│   │   ├── reports/
│   │   ├── settings/
│   │   └── compliance/
│   ├── api/
│   │   ├── auth/
│   │   ├── cleanup/
│   │   ├── reports/
│   │   ├── system/
│   │   └── config/
│   ├── globals.css
│   ├── layout.tsx
│   └── page.tsx
├── components/
│   ├── ui/
│   │   ├── button.tsx
│   │   ├── card.tsx
│   │   ├── input.tsx
│   │   ├── dialog.tsx
│   │   └── ...
│   ├── dashboard/
│   │   ├── SystemOverview.tsx
│   │   ├── CleanupStats.tsx
│   │   ├── ComplianceStatus.tsx
│   │   └── PerformanceMetrics.tsx
│   ├── cleanup/
│   │   ├── DirectorySelector.tsx
│   │   ├── ConfigurationEditor.tsx
│   │   ├── ScanResults.tsx
│   │   └── CleanupProgress.tsx
│   ├── reports/
│   │   ├── ReportGenerator.tsx
│   │   ├── ComplianceReport.tsx
│   │   ├── SecurityAudit.tsx
│   │   └── ExportOptions.tsx
│   └── layout/
│       ├── Header.tsx
│       ├── Sidebar.tsx
│       ├── Footer.tsx
│       └── Navigation.tsx
├── lib/
│   ├── api/
│   │   ├── client.ts
│   │   ├── cleanup.ts
│   │   ├── reports.ts
│   │   └── system.ts
│   ├── utils/
│   │   ├── validation.ts
│   │   ├── formatters.ts
│   │   └── helpers.ts
│   ├── hooks/
│   │   ├── useCleaner.ts
│   │   ├── useReports.ts
│   │   └── useConfig.ts
│   └── store/
│       ├── auth.ts
│       ├── cleanup.ts
│       └── config.ts
├── types/
│   ├── api.ts
│   ├── cleanup.ts
│   ├── reports.ts
│   └── system.ts
├── prisma/
│   ├── schema.prisma
│   └── migrations/
├── public/
│   ├── icons/
│   ├── images/
│   └── assets/
└── tests/
    ├── components/
    ├── api/
    └── e2e/
```

---

## 🎨 UI/UX Design System

### **Design Tokens**
```typescript
// design-tokens.ts
export const tokens = {
  colors: {
    primary: {
      50: '#eff6ff',
      100: '#dbeafe',
      500: '#3b82f6',
      600: '#2563eb',
      700: '#1d4ed8',
      900: '#1e3a8a',
    },
    secondary: {
      50: '#f8fafc',
      100: '#f1f5f9',
      500: '#64748b',
      600: '#475569',
      700: '#334155',
      900: '#0f172a',
    },
    success: {
      50: '#ecfdf5',
      500: '#10b981',
      600: '#059669',
    },
    warning: {
      50: '#fffbeb',
      500: '#f59e0b',
      600: '#d97706',
    },
    error: {
      50: '#fef2f2',
      500: '#ef4444',
      600: '#dc2626',
    },
  },
  typography: {
    fontFamily: {
      sans: ['Inter', 'system-ui', 'sans-serif'],
      mono: ['JetBrains Mono', 'monospace'],
    },
    fontSize: {
      xs: '0.75rem',
      sm: '0.875rem',
      base: '1rem',
      lg: '1.125rem',
      xl: '1.25rem',
      '2xl': '1.5rem',
      '3xl': '1.875rem',
    },
  },
  spacing: {
    xs: '0.25rem',
    sm: '0.5rem',
    md: '1rem',
    lg: '1.5rem',
    xl: '2rem',
    '2xl': '3rem',
  },
  borderRadius: {
    sm: '0.25rem',
    md: '0.375rem',
    lg: '0.5rem',
    xl: '0.75rem',
    full: '9999px',
  },
} as const;
```

### **Component Library**
```typescript
// components/ui/button.tsx
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost' | 'destructive';
  size?: 'sm' | 'md' | 'lg';
  loading?: boolean;
  icon?: React.ReactNode;
}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ variant = 'primary', size = 'md', loading, icon, children, ...props }, ref) => {
    // Implementation
  }
);
```

---

## 🔧 Core Features Implementation

### **1. Dashboard Overview**
```typescript
// components/dashboard/SystemOverview.tsx
interface SystemOverviewProps {
  systemInfo: SystemInfo;
  diskSpace: DiskSpaceInfo;
  cleanupStats: CleanupStats;
}

export const SystemOverview: React.FC<SystemOverviewProps> = ({
  systemInfo,
  diskSpace,
  cleanupStats,
}) => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <MetricCard
        title="System Health"
        value={systemInfo.healthScore}
        unit="%"
        trend={systemInfo.healthTrend}
        icon={<HealthIcon />}
      />
      <MetricCard
        title="Disk Usage"
        value={diskSpace.usagePercentage}
        unit="%"
        trend={diskSpace.trend}
        icon={<DiskIcon />}
      />
      <MetricCard
        title="Files Cleaned"
        value={cleanupStats.totalFiles}
        unit="files"
        trend={cleanupStats.trend}
        icon={<FileIcon />}
      />
      <MetricCard
        title="Space Freed"
        value={cleanupStats.spaceFreed}
        unit="GB"
        trend={cleanupStats.spaceTrend}
        icon={<StorageIcon />}
      />
    </div>
  );
};
```

### **2. Interactive Cleanup**
```typescript
// components/cleanup/DirectorySelector.tsx
interface DirectorySelectorProps {
  onDirectoriesChange: (directories: string[]) => void;
  selectedDirectories: string[];
}

export const DirectorySelector: React.FC<DirectorySelectorProps> = ({
  onDirectoriesChange,
  selectedDirectories,
}) => {
  const [directories, setDirectories] = useState<DirectoryNode[]>([]);
  const [loading, setLoading] = useState(false);

  const fetchDirectories = async () => {
    setLoading(true);
    try {
      const response = await api.getDirectories();
      setDirectories(response.data);
    } catch (error) {
      toast.error('Failed to fetch directories');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold">Select Directories</h3>
        <Button onClick={fetchDirectories} loading={loading}>
          Refresh
        </Button>
      </div>
      <DirectoryTree
        data={directories}
        selected={selectedDirectories}
        onSelectionChange={onDirectoriesChange}
      />
    </div>
  );
};
```

### **3. Real-time Progress Tracking**
```typescript
// components/cleanup/CleanupProgress.tsx
interface CleanupProgressProps {
  jobId: string;
  onComplete: (results: CleanupResults) => void;
}

export const CleanupProgress: React.FC<CleanupProgressProps> = ({
  jobId,
  onComplete,
}) => {
  const [progress, setProgress] = useState<CleanupProgress>({
    status: 'running',
    percentage: 0,
    currentFile: '',
    filesProcessed: 0,
    totalFiles: 0,
  });

  useEffect(() => {
    const eventSource = new EventSource(`/api/cleanup/progress/${jobId}`);
    
    eventSource.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setProgress(data);
      
      if (data.status === 'completed') {
        onComplete(data.results);
        eventSource.close();
      }
    };

    return () => eventSource.close();
  }, [jobId, onComplete]);

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <span className="text-sm font-medium">Progress</span>
        <span className="text-sm text-gray-500">
          {progress.filesProcessed} / {progress.totalFiles} files
        </span>
      </div>
      <ProgressBar value={progress.percentage} />
      <div className="text-sm text-gray-600">
        Processing: {progress.currentFile}
      </div>
    </div>
  );
};
```

---

## 🔌 API Integration

### **API Client Setup**
```typescript
// lib/api/client.ts
import axios from 'axios';

const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || '/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for authentication
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth-token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized access
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default apiClient;
```

### **Cleanup API**
```typescript
// lib/api/cleanup.ts
export const cleanupAPI = {
  // Scan directories
  scan: async (directories: string[], config?: CleanupConfig) => {
    const response = await apiClient.post('/cleanup/scan', {
      directories,
      config,
    });
    return response.data;
  },

  // Execute cleanup
  execute: async (scanId: string, options?: CleanupOptions) => {
    const response = await apiClient.post('/cleanup/execute', {
      scanId,
      options,
    });
    return response.data;
  },

  // Get cleanup status
  getStatus: async (jobId: string) => {
    const response = await apiClient.get(`/cleanup/status/${jobId}`);
    return response.data;
  },

  // Cancel cleanup
  cancel: async (jobId: string) => {
    const response = await apiClient.post(`/cleanup/cancel/${jobId}`);
    return response.data;
  },
};
```

---

## 🎯 Key Pages Implementation

### **Dashboard Page**
```typescript
// app/(dashboard)/dashboard/page.tsx
export default function DashboardPage() {
  const { data: systemInfo, isLoading } = useSystemInfo();
  const { data: cleanupStats } = useCleanupStats();
  const { data: complianceStatus } = useComplianceStatus();

  if (isLoading) {
    return <DashboardSkeleton />;
  }

  return (
    <div className="space-y-6">
      <PageHeader
        title="Dashboard"
        description="System overview and cleanup statistics"
      />
      
      <SystemOverview
        systemInfo={systemInfo}
        diskSpace={systemInfo.diskSpace}
        cleanupStats={cleanupStats}
      />
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <ComplianceStatus data={complianceStatus} />
        <PerformanceMetrics data={systemInfo.metrics} />
      </div>
      
      <RecentActivity />
    </div>
  );
}
```

### **Cleanup Page**
```typescript
// app/(dashboard)/cleanup/page.tsx
export default function CleanupPage() {
  const [selectedDirectories, setSelectedDirectories] = useState<string[]>([]);
  const [config, setConfig] = useState<CleanupConfig>(defaultConfig);
  const [scanResults, setScanResults] = useState<ScanResults | null>(null);
  const [isScanning, setIsScanning] = useState(false);

  const handleScan = async () => {
    setIsScanning(true);
    try {
      const results = await cleanupAPI.scan(selectedDirectories, config);
      setScanResults(results);
    } catch (error) {
      toast.error('Scan failed');
    } finally {
      setIsScanning(false);
    }
  };

  return (
    <div className="space-y-6">
      <PageHeader
        title="Cleanup"
        description="Scan and clean AppData directories"
      />
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Directory Selection</CardTitle>
          </CardHeader>
          <CardContent>
            <DirectorySelector
              selectedDirectories={selectedDirectories}
              onDirectoriesChange={setSelectedDirectories}
            />
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader>
            <CardTitle>Configuration</CardTitle>
          </CardHeader>
          <CardContent>
            <ConfigurationEditor
              config={config}
              onConfigChange={setConfig}
            />
          </CardContent>
        </Card>
      </div>
      
      {scanResults && (
        <ScanResults
          results={scanResults}
          onExecute={handleExecute}
        />
      )}
    </div>
  );
}
```

---

## 🔒 Security Implementation

### **Authentication**
```typescript
// lib/auth.ts
import { NextAuthOptions } from 'next-auth';
import CredentialsProvider from 'next-auth/providers/credentials';

export const authOptions: NextAuthOptions = {
  providers: [
    CredentialsProvider({
      name: 'credentials',
      credentials: {
        username: { label: 'Username', type: 'text' },
        password: { label: 'Password', type: 'password' },
      },
      async authorize(credentials) {
        // Implement authentication logic
        const user = await authenticateUser(credentials);
        return user;
      },
    }),
  ],
  session: {
    strategy: 'jwt',
  },
  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        token.role = user.role;
        token.permissions = user.permissions;
      }
      return token;
    },
    async session({ session, token }) {
      session.user.role = token.role;
      session.user.permissions = token.permissions;
      return session;
    },
  },
};
```

### **Authorization Middleware**
```typescript
// middleware.ts
import { withAuth } from 'next-auth/middleware';
import { NextResponse } from 'next/server';

export default withAuth(
  function middleware(req) {
    const token = req.nextauth.token;
    const { pathname } = req.nextUrl;

    // Check permissions based on route
    if (pathname.startsWith('/admin') && token?.role !== 'admin') {
      return NextResponse.redirect(new URL('/unauthorized', req.url));
    }

    return NextResponse.next();
  },
  {
    callbacks: {
      authorized: ({ token }) => !!token,
    },
  }
);

export const config = {
  matcher: ['/dashboard/:path*', '/admin/:path*'],
};
```

---

## 📊 State Management

### **Zustand Store**
```typescript
// lib/store/cleanup.ts
import { create } from 'zustand';
import { devtools } from 'zustand/middleware';

interface CleanupState {
  currentJob: CleanupJob | null;
  scanResults: ScanResults | null;
  config: CleanupConfig;
  isScanning: boolean;
  isCleaning: boolean;
  
  // Actions
  setCurrentJob: (job: CleanupJob | null) => void;
  setScanResults: (results: ScanResults | null) => void;
  setConfig: (config: CleanupConfig) => void;
  setScanning: (scanning: boolean) => void;
  setCleaning: (cleaning: boolean) => void;
  reset: () => void;
}

export const useCleanupStore = create<CleanupState>()(
  devtools(
    (set) => ({
      currentJob: null,
      scanResults: null,
      config: defaultConfig,
      isScanning: false,
      isCleaning: false,

      setCurrentJob: (job) => set({ currentJob: job }),
      setScanResults: (results) => set({ scanResults: results }),
      setConfig: (config) => set({ config }),
      setScanning: (scanning) => set({ isScanning: scanning }),
      setCleaning: (cleaning) => set({ isCleaning: cleaning }),
      reset: () => set({
        currentJob: null,
        scanResults: null,
        config: defaultConfig,
        isScanning: false,
        isCleaning: false,
      }),
    }),
    { name: 'cleanup-store' }
  )
);
```

---

## 🧪 Testing Strategy

### **Unit Tests**
```typescript
// tests/components/DirectorySelector.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { DirectorySelector } from '@/components/cleanup/DirectorySelector';

describe('DirectorySelector', () => {
  it('renders directory tree correctly', () => {
    const mockDirectories = [
      { id: '1', name: 'AppData', path: 'C:\\Users\\Admin\\AppData' },
      { id: '2', name: 'Local', path: 'C:\\Users\\Admin\\AppData\\Local' },
    ];

    render(
      <DirectorySelector
        selectedDirectories={[]}
        onDirectoriesChange={jest.fn()}
      />
    );

    expect(screen.getByText('Select Directories')).toBeInTheDocument();
  });

  it('calls onDirectoriesChange when directories are selected', () => {
    const mockOnChange = jest.fn();
    
    render(
      <DirectorySelector
        selectedDirectories={[]}
        onDirectoriesChange={mockOnChange}
      />
    );

    const checkbox = screen.getByRole('checkbox');
    fireEvent.click(checkbox);

    expect(mockOnChange).toHaveBeenCalledWith(['C:\\Users\\Admin\\AppData']);
  });
});
```

### **E2E Tests**
```typescript
// tests/e2e/cleanup.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Cleanup Flow', () => {
  test('should complete full cleanup process', async ({ page }) => {
    // Navigate to cleanup page
    await page.goto('/cleanup');
    
    // Select directories
    await page.click('[data-testid="directory-checkbox"]');
    
    // Configure cleanup
    await page.fill('[data-testid="config-input"]', 'test-config');
    
    // Start scan
    await page.click('[data-testid="scan-button"]');
    
    // Wait for scan completion
    await expect(page.locator('[data-testid="scan-results"]')).toBeVisible();
    
    // Execute cleanup
    await page.click('[data-testid="execute-button"]');
    
    // Verify completion
    await expect(page.locator('[data-testid="completion-message"]')).toBeVisible();
  });
});
```

---

## 🚀 Deployment Configuration

### **Vercel Configuration**
```json
// vercel.json
{
  "version": 2,
  "builds": [
    {
      "src": "package.json",
      "use": "@vercel/next"
    }
  ],
  "env": {
    "DATABASE_URL": "@database-url",
    "NEXTAUTH_SECRET": "@nextauth-secret",
    "NEXTAUTH_URL": "@nextauth-url"
  },
  "functions": {
    "app/api/**/*.ts": {
      "maxDuration": 30
    }
  }
}
```

### **Environment Variables**
```bash
# .env.local
DATABASE_URL="postgresql://user:password@localhost:5432/cleaner"
NEXTAUTH_SECRET="your-secret-key"
NEXTAUTH_URL="http://localhost:3000"
NEXT_PUBLIC_API_URL="http://localhost:3000/api"
```

---

## 📈 Performance Optimization

### **Code Splitting**
```typescript
// Dynamic imports for heavy components
const DirectorySelector = dynamic(() => import('@/components/cleanup/DirectorySelector'), {
  loading: () => <DirectorySelectorSkeleton />,
  ssr: false,
});

const ReportGenerator = dynamic(() => import('@/components/reports/ReportGenerator'), {
  loading: () => <ReportGeneratorSkeleton />,
});
```

### **Caching Strategy**
```typescript
// lib/cache.ts
import { unstable_cache } from 'next/cache';

export const getSystemInfo = unstable_cache(
  async () => {
    // Fetch system information
    return await api.getSystemInfo();
  },
  ['system-info'],
  {
    revalidate: 300, // 5 minutes
    tags: ['system'],
  }
);
```

This comprehensive specification provides a detailed roadmap for building a modern, scalable Next.js web application around your enterprise AppData cleaner. 