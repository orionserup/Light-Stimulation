/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.c
  * @brief          : Main program body
  ******************************************************************************
  * @attention
  *
  * <h2><center>&copy; Copyright (c) 2020 STMicroelectronics.
  * All rights reserved.</center></h2>
  *
  * This software component is licensed by ST under BSD 3-Clause license,
  * the "License"; You may not use this file except in compliance with the
  * License. You may obtain a copy of the License at:
  *                        opensource.org/licenses/BSD-3-Clause
  *
  ******************************************************************************
  */
/* USER CODE END Header */

/* Includes ------------------------------------------------------------------*/
#include "main.h"
#include <stdint.h>

/* Private includes ----------------------------------------------------------*/

void SystemClock_Config(void);
static void MX_GPIO_Init(void);
static void MX_RTC_Init(void);
static void MX_TIM_Init(void);
static void WAIT(int minutes);
static void SET_LED(short ir, short red);
static void INC_COUNTER(void);
static void erasepage(int page);
static void writeparamstoNVM(int red, int ir, int ontime, int offtime, int redarr, int irarr);

static unsigned short GET_RED(unsigned int ARR);
static unsigned short GET_IR(unsigned int ARR);
static unsigned short GET_RED_ARR(void);
static unsigned short GET_IR_ARR(void);
static unsigned short GET_ONTIME(void);
static unsigned short GET_OFFTIME(void);

RTC_HandleTypeDef hrtc;
TIM_HandleTypeDef htim2;
TIM_HandleTypeDef htim15;

/* USER CODE BEGIN Includes */
uint64_t* COUNTER_ADDRESS = (uint64_t*)0x0800d000;
uint32_t COUNTER_PAGE = 26;

volatile uint64_t* RED_ADDRESS =     (uint64_t*)0x0800c000;
volatile uint64_t* IR_ADDRESS =      (uint64_t*)0x0800c800;
volatile uint64_t* ONTIME_ADDRESS =  (uint64_t*)0x0800e000;
volatile uint64_t* OFFTIME_ADDRESS = (uint64_t*)0x0800e800;
volatile uint64_t* RED_FREQ_ADDRESS =(uint64_t*)0x0800f000;
volatile uint64_t* IR_FREQ_ADDRESS = (uint64_t*)0x0800f800;

#define TIM_FREQ 10000

/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void)
{
 
  HAL_Init();
  SystemClock_Config();
  MX_GPIO_Init();
  MX_RTC_Init();
	MX_TIM_Init();
	
	uint16_t ir, red, ontime, offtime, redarrvalue, irarrvalue;
	
	redarrvalue = GET_RED_ARR();
	TIM15->ARR = redarrvalue;
	
	irarrvalue = GET_IR_ARR();
	TIM2->ARR = irarrvalue;
	
	red = GET_RED(redarrvalue);
	ir = GET_IR(irarrvalue);
	
	ontime = GET_ONTIME();
	offtime = GET_OFFTIME();
	
  while (1){
		
		SET_LED(ir, red);
		WAIT(ontime);
		INC_COUNTER();
		
		SET_LED(0, 0);
		WAIT(offtime);
 
  }
}

void SET_LED(short ir, short red){
	
	TIM2->CCR2 = ir;
	TIM15->CCR1 = red;
	
}


void erasepage(int page){
	
	FLASH_EraseInitTypeDef erase;
	
	erase.Page = page;
	erase.TypeErase = FLASH_TYPEERASE_PAGES;
	erase.NbPages = 1;
	
	unsigned int error = 0;
	
	HAL_FLASH_Unlock();
	HAL_FLASHEx_Erase(&erase, &error);
	HAL_FLASH_Lock();
}



unsigned short GET_IR( unsigned int ARR ){
	
	uint64_t ir = *IR_ADDRESS;
	
	return (unsigned short)(ARR * (unsigned char)ir)/100;
	
}

unsigned short GET_RED( unsigned int ARR ){
	
	uint64_t red = *RED_ADDRESS;
	
	return (unsigned short)(ARR * (unsigned char)red)/100;
	
}

unsigned short GET_RED_ARR(){
	
	uint64_t redfreq = *RED_FREQ_ADDRESS;
	
	return (uint16_t)(TIM_FREQ/(unsigned char)redfreq) - 1;  // if an actual value then return the corresponding value
	
}

unsigned short GET_IR_ARR(){
	
	uint64_t irfreq = *IR_FREQ_ADDRESS;
	
	return (uint16_t)(TIM_FREQ/(unsigned char)irfreq) - 1;
	
}

unsigned short GET_ONTIME(){
	
	uint64_t ontime = *ONTIME_ADDRESS;
	
	return (uint16_t)ontime;
	
}

unsigned short GET_OFFTIME(){
	
	uint64_t offtime = *OFFTIME_ADDRESS;
	
	return (uint16_t)offtime;
	
}

void WAIT(int minutes){
	
	RTC_TimeTypeDef time = {0};
	RTC_DateTypeDef date = {0};
	
	HAL_RTC_SetTime(&hrtc, &time, RTC_FORMAT_BCD);
	HAL_RTC_SetDate(&hrtc, &date, RTC_FORMAT_BCD);
	
	while(time.Minutes < minutes){
		HAL_RTC_GetTime(&hrtc, &time, RTC_FORMAT_BCD);
		HAL_RTC_GetDate(&hrtc, &date, RTC_FORMAT_BCD);
	}
	
}

void INC_COUNTER(){

	uint64_t counter = *(uint64_t*)COUNTER_ADDRESS;
	
	HAL_FLASH_Unlock();
	if(counter != 0xffffffffffffffff) erasepage(COUNTER_PAGE);
	HAL_FLASH_Program(FLASH_TYPEPROGRAM_DOUBLEWORD, (uint32_t)COUNTER_ADDRESS, ++counter);
	HAL_FLASH_Lock();
	
}

/**
  * @brief System Clock Configuration
  * @retval None
  */
void SystemClock_Config(void)
{
  RCC_OscInitTypeDef RCC_OscInitStruct = {0};
  RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};
  RCC_PeriphCLKInitTypeDef PeriphClkInit = {0};

  /** Configure the main internal regulator output voltage 
  */
  HAL_PWREx_ControlVoltageScaling(PWR_REGULATOR_VOLTAGE_SCALE1);
	/* Initializes the CPU, AHB and APB busses clocks 
  */
  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_LSI|RCC_OSCILLATORTYPE_MSI;
  RCC_OscInitStruct.LSIState = RCC_LSI_ON;
  RCC_OscInitStruct.MSIState = RCC_MSI_ON;
  RCC_OscInitStruct.MSICalibrationValue = 0;
  RCC_OscInitStruct.MSIClockRange = RCC_MSIRANGE_6;
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_NONE;
  
	HAL_RCC_OscConfig(&RCC_OscInitStruct);
  /** Initializes the CPU, AHB and APB busses clocks 
  */
  RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK
                              |RCC_CLOCKTYPE_PCLK1|RCC_CLOCKTYPE_PCLK2;
  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_MSI;
  RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV1;
  RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV1;

  HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_0);
	
  PeriphClkInit.PeriphClockSelection = RCC_PERIPHCLK_RTC;
  PeriphClkInit.RTCClockSelection = RCC_RTCCLKSOURCE_LSI;
  
	HAL_RCCEx_PeriphCLKConfig(&PeriphClkInit);
}

/**
  * @brief RTC Initialization Function
  * @param None
  * @retval None
  */
static void MX_RTC_Init(void)
{

  RTC_TimeTypeDef sTime = {0};
  RTC_DateTypeDef sDate = {0};

  hrtc.Instance = RTC;
  hrtc.Init.HourFormat = RTC_HOURFORMAT_24;
  hrtc.Init.AsynchPrediv = 127;
  hrtc.Init.SynchPrediv = 255;
  hrtc.Init.OutPut = RTC_OUTPUT_DISABLE;
  hrtc.Init.OutPutRemap = RTC_OUTPUT_REMAP_NONE;
  hrtc.Init.OutPutPolarity = RTC_OUTPUT_POLARITY_HIGH;
  hrtc.Init.OutPutType = RTC_OUTPUT_TYPE_OPENDRAIN;
  hrtc.Init.OutPutPullUp = RTC_OUTPUT_PULLUP_NONE;
  
	HAL_RTC_Init(&hrtc);
	
  sTime.Hours = 0x0;
  sTime.Minutes = 0x0;
  sTime.Seconds = 0x0;
  sTime.DayLightSaving = RTC_DAYLIGHTSAVING_NONE;
  sTime.StoreOperation = RTC_STOREOPERATION_RESET;
  
	HAL_RTC_SetTime(&hrtc, &sTime, RTC_FORMAT_BCD);
	
  sDate.WeekDay = RTC_WEEKDAY_MONDAY;
  sDate.Month = RTC_MONTH_JANUARY;
  sDate.Date = 0x1;
  sDate.Year = 0x0;

  HAL_RTC_SetDate(&hrtc, &sDate, RTC_FORMAT_BCD);

}

/**
  * @brief TIM2 Initialization Function
  * @param None
  * @retval None
  */
static void MX_TIM_Init(void)
{

  TIM_ClockConfigTypeDef sClockSourceConfig = {0};
  TIM_MasterConfigTypeDef sMasterConfig = {0};
  TIM_OC_InitTypeDef sConfigOC = {0};
	
	HAL_TIM_Base_MspInit(&htim2);
	HAL_TIM_Base_MspInit(&htim15);

  htim2.Instance = TIM2;
  htim2.Init.Prescaler = 399;
  htim2.Init.CounterMode = TIM_COUNTERMODE_UP;
  htim2.Init.Period = 1;
  htim2.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
  htim2.Init.AutoReloadPreload = TIM_AUTORELOAD_PRELOAD_ENABLE;
	
	htim15.Instance = TIM15;
  htim15.Init.Prescaler = 399;
  htim15.Init.CounterMode = TIM_COUNTERMODE_UP;
  htim15.Init.Period = 1;
  htim15.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
  htim15.Init.AutoReloadPreload = TIM_AUTORELOAD_PRELOAD_ENABLE;
  
	HAL_TIM_Base_Init(&htim2);
	HAL_TIM_Base_Init(&htim15);
	
  sClockSourceConfig.ClockSource = TIM_CLOCKSOURCE_INTERNAL;
  
	HAL_TIM_ConfigClockSource(&htim2, &sClockSourceConfig);
	HAL_TIM_ConfigClockSource(&htim15, &sClockSourceConfig);
	
	HAL_TIM_PWM_Init(&htim2);
	HAL_TIM_PWM_Init(&htim15);
	
  sMasterConfig.MasterOutputTrigger = TIM_TRGO_RESET;
  sMasterConfig.MasterSlaveMode = TIM_MASTERSLAVEMODE_DISABLE;
  
	HAL_TIMEx_MasterConfigSynchronization(&htim2, &sMasterConfig);
	HAL_TIMEx_MasterConfigSynchronization(&htim15, &sMasterConfig);
	
  sConfigOC.OCMode = TIM_OCMODE_PWM1;
  sConfigOC.Pulse = 50;
  sConfigOC.OCPolarity = TIM_OCPOLARITY_HIGH;
  sConfigOC.OCFastMode = TIM_OCFAST_ENABLE;
	
	HAL_TIM_MspPostInit(&htim2);
	HAL_TIM_MspPostInit(&htim15);

	HAL_TIM_PWM_ConfigChannel(&htim2, &sConfigOC, TIM_CHANNEL_2);
	HAL_TIM_PWM_ConfigChannel(&htim15, &sConfigOC, TIM_CHANNEL_1);
	
	HAL_TIM_Base_Start(&htim2);
	HAL_TIM_Base_Start(&htim15);
	
	HAL_TIM_PWM_Start(&htim2, TIM_CHANNEL_2);
	HAL_TIM_PWM_Start(&htim15, TIM_CHANNEL_1);
	
	
}

/* USER CODE BEGIN TIM2_Init 0 */

/**
  * @brief GPIO Initialization Function
  * @param None
  * @retval None
  */
static void MX_GPIO_Init(void)
{

  /* GPIO Ports Clock Enable */
  __HAL_RCC_GPIOA_CLK_ENABLE();

}
